resource "helm_release" "mosquitto" {
  name       = "mosquitto"
  repository = "https://naps.github.io/helm-charts/"
  chart      = "mosquitto"

  set {
    name  = "service.ports.mqtt"
    value = var.mqtt_port
  }
  set {
    name = "mosquitto.config"
    value = <<EOT
allow_anonymous true
log_type all
EOT
  }

  set {
    name = "mosquitto.persistence.enabled"
    value = true
  }
}
