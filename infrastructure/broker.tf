resource "helm_release" "mosquitto" {
  name       = "mosquitto"
  repository = "https://naps.github.io/helm-charts/"
  chart      = "mosquitto"

  set {
    name  = "service.ports.mqtt"
    value = var.mqtt_port
  }
}
