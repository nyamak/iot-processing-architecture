resource "kubernetes_deployment" "notifier" {
  metadata {
    name = "notifier"
  }

  lifecycle {
    ignore_changes = [
      spec[0].replicas,
    ]
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "notifier"
      }
    }

    template {
      metadata {
        labels = {
          app = "notifier"
        }
      }

      spec {
        termination_grace_period_seconds = 30
        container {
          image             = var.notifier_image_url
          name              = "notifier"
          image_pull_policy = "Always"

          port {
            container_port = var.notifier_service_port
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }

          env_from {
            config_map_ref {
              name = kubernetes_config_map.notifier.metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.notifier.metadata[0].name
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "notifier" {
  metadata {
    name = "notifier"
  }
  spec {
    selector = {
      app = kubernetes_deployment.notifier.spec.0.template.0.metadata.0.labels.app
    }
    type = "ClusterIP"
    port {
      port = var.notifier_service_port
    }
  }
}

resource "kubernetes_config_map" "notifier" {
  metadata {
    name = "notifier"
  }
  data = {
    SENGRID_FROM_EMAIL = var.sendgrid_from_email
    SENDGRID_TO_EMAIL  = var.sendgrid_to_email
    PORT               = var.notifier_service_port
  }
}

resource "kubernetes_secret" "notifier" {
  metadata {
    name = "notifier"
  }
  data = {
    SENDGRID_API_KEY = var.sendgrid_api_key
  }
}
