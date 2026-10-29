variable "project_id" {
  description = "Your GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west4" # Netherlands
}

variable "image" {
  description = "Full Docker image path. Leave empty on the first apply."
  type        = string
  default     = ""
}

variable "allow_public" {
  description = "Allow unauthenticated access (demo only)"
  type        = bool
  default     = true
}
