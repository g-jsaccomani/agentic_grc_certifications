output "folder_id" {
  description = "Resource name of the created GRC folder"
  value       = google_folder.grc_folder.name
}

output "project_id" {
  description = "Project ID of the newly provisioned GRC host project"
  value       = google_project.grc_project.project_id
}

output "auditor_service_account_email" {
  description = "Email address of the auditor service account with organization-wide read access"
  value       = google_service_account.grc_auditor.email
}

output "region" {
  description = "Target deployment region"
  value       = var.region
}

output "next_step_deploy_commands" {
  description = "Commands to copy and run for deploying the Agentic GRC platform"
  value       = <<-EOT
    # 1. Authenticate to Google Cloud
    gcloud auth login
    gcloud auth application-default login

    # 2. Navigate to the repository root
    cd agentic_grc_certifications

    # 3. Export environment variables
    export PROJECT_ID="${google_project.grc_project.project_id}"
    export REGION="${var.region}"

    # 4. Deploy the Agent and Client Portal
    make journey
  EOT
}
