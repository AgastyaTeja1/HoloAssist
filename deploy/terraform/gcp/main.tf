provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region
  initial_node_count = 1

  node_config {
    machine_type = "n1-standard-4"
    oauth_scopes = ["cloud-platform"]
  }

  node_pool {
    name       = "gpu-pool"
    initial_node_count = 1
    node_config {
      machine_type = "n1-standard-4"
      guest_accelerator {
        type  = "nvidia-tesla-t4"
        count = 1
      }
    }
    autoscaling {
      min_node_count = 1
      max_node_count = 3
    }
  }
}
