terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

locals {
  apis       = ["run.googleapis.com", "artifactregistry.googleapis.com", "cloudbuild.googleapis.com"]
  deploy_api = var.image != ""
}

# Turn on the GCP services we need.
resource "google_project_service" "apis" {
  for_each           = toset(local.apis)
  service            = each.key
  disable_on_destroy = false
}

# Private registry that stores our Docker image.
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = "noshow"
  format        = "DOCKER"
  depends_on    = [google_project_service.apis]
}

# The API. Only created once an image is provided (see DEPLOY.md).
resource "google_cloud_run_v2_service" "api" {
  count               = local.deploy_api ? 1 : 0
  name                = "noshow-predictor"
  location            = var.region
  deletion_protection = false

  template {
    scaling {
      min_instance_count = 0 # scale to zero = no cost when idle
      max_instance_count = 2 # cap cost and blast radius
    }
    containers {
      image = var.image
      ports {
        container_port = 8080
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "1Gi"
        }
      }
      startup_probe {
        http_get {
          path = "/health"
        }
      }
    }
  }

  depends_on = [google_project_service.apis]
}

# Public access for the demo. Set allow_public = false to require auth.
resource "google_cloud_run_v2_service_iam_member" "public" {
  count    = local.deploy_api && var.allow_public ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.api[0].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
