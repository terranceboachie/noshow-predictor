output "registry_path" {
  value = "${var.region}-docker.pkg.dev/${var.project_id}/noshow"
}

output "service_url" {
  value = local.deploy_api ? google_cloud_run_v2_service.api[0].uri : "not deployed yet"
}
