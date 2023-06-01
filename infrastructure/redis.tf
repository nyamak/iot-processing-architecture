resource "helm_release" "notifier_cache" {
  name       = "notifier-cache"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "redis"

  set {
    name  = "auth.enabled"
    value = "false"
  }

  set {
    name  = "architecture"
    value = "standalone"
  }
  set {
    name  = "master.service.ports.redis"
    value = var.notifier_cache_port
  }
}
