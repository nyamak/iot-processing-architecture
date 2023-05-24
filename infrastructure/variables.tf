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

variable "metrics_db_host" {
  type        = string
  description = "Metrics DB host."
  default     = "metrics"
}

variable "metrics_db_port" {
  type        = number
  description = "Metrics DB port."
  default     = 27017
}

# Processor service variables
variable "processor_image_url" {
  type        = string
  description = "Docker image URL for Processor."
}

variable "processor_target_cpu_utilization_percentage" {
  type        = number
  description = "Target CPU utilization percentage for Processor service."
  default     = 80
}

variable "processor_service_host" {
  type        = string
  description = "Host for Processor service."
  default     = "processor"
}

variable "processor_service_port" {
  type        = number
  description = "Port for Processor service."
  default     = 5000
}

variable "processor_service_max_replicas" {
  type        = number
  description = "Maximum replicas of processor service."
  default     = 3
}

variable "processor_service_min_replicas" {
  type        = number
  description = "Minimum replicas of processor service."
  default     = 1
}

variable "temperature_limit" {
  type        = number
  description = "Temperature threshold for machines."
  default     = 75
}

variable "pressure_limit" {
  type        = number
  description = "Pressure threshold for machines."
  default     = 1.0
}

variable "defective_limit" {
  type        = number
  description = "Defective percentage threshold for machines."
  default     = 5.0
}

# Notifier service variables
variable "notifier_image_url" {
  type        = string
  description = "Docker image URL for Notifier service."
}

variable "notifier_service_host" {
  type        = string
  description = "Host for Notifier service."
  default     = "notifier"
}

variable "notifier_service_port" {
  type        = number
  description = "Port for Notifier service."
  default     = 5000
}

# MQTT broker variables
variable "mqtt_host" {
  type        = string
  description = "Host for MQTT broker."
  default     = "mosquitto"
}

variable "mqtt_port" {
  type        = number
  description = "Port for MQTT broker."
  default     = 1883
}

variable "mqtt_topic" {
  type        = string
  description = "Topic for MQTT broker."
  default     = "payloads"
}

# Sendgrid variables
variable "sendgrid_api_key" {
  type        = string
  description = "API key for Sendgrid."
  sensitive   = true
}

variable "sendgrid_from_email" {
  type        = string
  description = "From Email on Sendgrid."
}

variable "sendgrid_to_email" {
  type        = string
  description = "To Email on Sendgrid."
}
