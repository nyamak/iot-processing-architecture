resource "helm_release" "metrics_db" {
  name       = "metrics-db"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "postgresql"

  set {
    name  = "auth.username"
    value = var.metrics_db_username
  }

  set {
    name  = "auth.password"
    value = var.metrics_db_password
  }

  set {
    name  = "auth.database"
    value = var.metrics_db_name
  }

  set {
    name  = "architecture"
    value = "standalone"
  }

  set {
    name  = "primary.service.ports.postgresql"
    value = var.metrics_db_port
  }
}
