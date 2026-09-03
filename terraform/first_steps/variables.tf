variable "org_id" {
  description = "GCP Organization ID (numeric string, e.g. 31564119954)"
  type        = string
  default     = "31564119954"
}

variable "billing_account" {
  description = "GCP Billing Account ID (format: XXXXXX-XXXXXX-XXXXXX)"
  type        = string
  default     = "0180FF-1553BD-6B74BE"
}

variable "folder_name" {
  description = "Display name for the dedicated GRC folder to create under the organization"
  type        = string
  default     = "fldr-agentic-grc"
}

variable "project_prefix" {
  description = "Prefix for the newly created GCP project ID"
  type        = string
  default     = "agentic-grc"
}

variable "custom_project_id" {
  description = "Optional explicit project ID. If empty, a random suffix is appended to project_prefix."
  type        = string
  default     = ""
}

variable "region" {
  description = "Default Google Cloud region for services"
  type        = string
  default     = "us-central1"
}

variable "service_account_name" {
  description = "Service account ID for the autonomous GRC auditor"
  type        = string
  default     = "sa-agentic-grc-auditor"
}

variable "deployer_email" {
  description = "Email address of the engineer/consultant deploying the platform (e.g. jsaccomani@google.com)"
  type        = string
  default     = "jsaccomani@google.com"
}

variable "required_apis" {
  description = "Google Cloud APIs required by the Agentic GRC platform"
  type        = list(string)
  default = [
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iam.googleapis.com",
    "modelarmor.googleapis.com",
    "run.googleapis.com",
    "cloudasset.googleapis.com",
    "securitycenter.googleapis.com",
    "accesscontextmanager.googleapis.com",
    "cloudkms.googleapis.com",
    "bigquery.googleapis.com",
    "aiplatform.googleapis.com",
    "discoveryengine.googleapis.com",
    "artifactregistry.googleapis.com",
    "cloudbuild.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ]
}

variable "org_roles" {
  description = "Organization-level IAM roles granted to the auditor service account"
  type        = list(string)
  default = [
    "roles/cloudasset.viewer",
    "roles/browser",
    "roles/iam.securityReviewer",
    "roles/securitycenter.findingsViewer",
    "roles/accesscontextmanager.policyReader"
  ]
}

variable "deployer_project_roles" {
  description = "Project-level roles granted to the deployer engineer"
  type        = list(string)
  default = [
    "roles/viewer",
    "roles/run.admin",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.admin",
    "roles/storage.admin",
    "roles/aiplatform.user",
    "roles/serviceusage.serviceUsageConsumer",
    "roles/cloudbuild.builds.editor"
  ]
}
