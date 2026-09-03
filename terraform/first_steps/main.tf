terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}

provider "google" {
  region = var.region
}

# ------------------------------------------------------------------------------
# 1. Organization Folder
# ------------------------------------------------------------------------------
resource "google_folder" "grc_folder" {
  display_name = var.folder_name
  parent       = "organizations/${var.org_id}"
}

# ------------------------------------------------------------------------------
# 2. Host Project under the Dedicated Folder
# ------------------------------------------------------------------------------
resource "random_id" "project_suffix" {
  byte_length = 2
}

locals {
  project_id = var.custom_project_id != "" ? var.custom_project_id : "${var.project_prefix}-${random_id.project_suffix.hex}"
}

resource "google_project" "grc_project" {
  name                = "Agentic GRC Platform"
  project_id          = local.project_id
  folder_id           = google_folder.grc_folder.folder_id
  billing_account     = var.billing_account
  auto_create_network = false
}

# ------------------------------------------------------------------------------
# 3. Google Cloud APIs Enablement
# ------------------------------------------------------------------------------
resource "google_project_service" "apis" {
  for_each = toset(var.required_apis)

  project = google_project.grc_project.project_id
  service = each.value

  disable_on_destroy = false
}

# ------------------------------------------------------------------------------
# 4. Auditor Service Account
# ------------------------------------------------------------------------------
resource "google_service_account" "grc_auditor" {
  account_id   = var.service_account_name
  display_name = "Agentic GRC Org Auditor"
  description  = "Autonomous audit identity with organization-level read privileges"
  project      = google_project.grc_project.project_id

  depends_on = [google_project_service.apis]
}

# ------------------------------------------------------------------------------
# 5. Organization-Level IAM Roles Granted to Auditor Service Account
# ------------------------------------------------------------------------------
resource "google_organization_iam_member" "org_roles" {
  for_each = toset(var.org_roles)

  org_id = var.org_id
  role   = each.value
  member = "serviceAccount:${google_service_account.grc_auditor.email}"
}

# ------------------------------------------------------------------------------
# 6. Deployer IAM Permissions on Host Project (for Engineer make journey execution)
# ------------------------------------------------------------------------------
locals {
  # Merge legacy deployer_email (if present) with deployer_emails list
  raw_deployer_list = distinct(concat(
    var.deployer_email != "" ? [var.deployer_email] : [],
    var.deployer_emails
  ))

  # Ensure each entry is prefixed with IAM member type (defaults to user: if not specified)
  formatted_deployer_members = [
    for m in local.raw_deployer_list : (
      can(regex("^(user|serviceAccount|group|domain):", m)) ? m : "user:${m}"
    )
  ]

  # Matrix product of members and roles
  deployer_member_roles = flatten([
    for m in local.formatted_deployer_members : [
      for r in var.deployer_project_roles : {
        key    = "${m}-${r}"
        member = m
        role   = r
      }
    ]
  ])
}

resource "google_project_iam_member" "deployer_roles" {
  for_each = {
    for item in local.deployer_member_roles : item.key => item
  }

  project = google_project.grc_project.project_id
  role    = each.value.role
  member  = each.value.member

  depends_on = [google_project_service.apis]
}

resource "google_service_account_iam_member" "deployer_sa_user" {
  for_each = toset(local.formatted_deployer_members)

  service_account_id = google_service_account.grc_auditor.name
  role               = "roles/iam.serviceAccountUser"
  member             = each.value

  depends_on = [google_service_account.grc_auditor]
}

# ------------------------------------------------------------------------------
# 7. Cloud Build & Compute Default Service Account (for Cloud Run source builds)
# ------------------------------------------------------------------------------
resource "google_project_iam_member" "compute_sa_builder_roles" {
  for_each = toset([
    "roles/storage.admin",
    "roles/logging.logWriter",
    "roles/artifactregistry.writer"
  ])

  project = google_project.grc_project.project_id
  role    = each.value
  member  = "serviceAccount:${google_project.grc_project.number}-compute@developer.gserviceaccount.com"

  depends_on = [google_project_service.apis]
}
