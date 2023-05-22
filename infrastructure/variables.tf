# Metrics DB
variable "metrics_db_username" {
  type        = string
  sensitive   = true
  description = "Metrics DB username"
}

variable "metrics_db_password" {
  type        = string
  sensitive   = true
  description = "Metrics DB passwword."
}

variable "metrics_db_name" {
  type        = string
  description = "Metrics DB username."
  default     = "metrics"
}

variable "metrics_db_port" {
  type        = number
  description = "Metrics DB port."
  default     = 27017
}
