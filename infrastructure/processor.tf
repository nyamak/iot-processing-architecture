resource "kubernetes_deployment" "processor" {
  metadata {
    name = "processor"
  }

  lifecycle {
    ignore_changes = [
      spec[0].replicas,
    ]
  }

  depends_on = [kubernetes_deployment.notifier, helm_release.metrics_db]

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "processor"
      }
    }

    template {
      metadata {
        labels = {
          app = "processor"
        }
      }

      spec {
        termination_grace_period_seconds = 30
        container {
          image             = var.processor_image_url
          name              = "processor"
          image_pull_policy = "Always"

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
              name = kubernetes_config_map.processor.metadata[0].name
            }
          }
          env_from {
            secret_ref {
              name = kubernetes_secret.processor.metadata[0].name
            }
          }
        }
      }
    }
  }
}
resource "kubernetes_config_map" "processor" {
  metadata {
    name = "processor"
  }
  data = {
    MQTT_HOST                = var.mqtt_host
    MQTT_PORT                = var.mqtt_port
    MQTT_TOPIC               = var.mqtt_topic
    DB_HOST                  = var.metrics_db_host
    DB_PORT                  = var.metrics_db_port
    DB_NAME                  = var.metrics_db_name
    PRESSURE_LIMIT           = var.pressure_limit
    TEMPERATURE_LIMIT        = var.temperature_limit
    DEFECTIVE_LIMIT          = var.defective_limit
    NOTIFIER_HOST            = var.notifier_service_host
    NOTIFIER_PORT            = var.notifier_service_port
    NOTIFICATION_TIME_WINDOW = var.notification_time_window
    ENV                      = var.env
  }
}

resource "kubernetes_secret" "processor" {
  metadata {
    name = "processor"
  }
  data = {
    DB_USER     = var.metrics_db_username
    DB_PASSWORD = var.metrics_db_password
  }
}

resource "kubernetes_horizontal_pod_autoscaler_v2" "processor" {
  metadata {
    name = "processor"
  }

  spec {
    max_replicas = var.processor_service_max_replicas
    min_replicas = var.processor_service_min_replicas

    scale_target_ref {
      kind        = "Deployment"
      name        = "processor"
      api_version = "apps/v1"
    }

    metric {
      type = "Resource"
      resource {
        name = "memory"
        target {
          type                = "Utilization"
          average_utilization = var.processor_average_memory
        }
      }
    }
  }
}
