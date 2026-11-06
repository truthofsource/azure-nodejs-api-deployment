variable "name" {
  type = string
}

variable "resource_group_name" {
  type = string
}

variable "location" {
  type = string
}

variable "service_plan_id" {
  type = string
}

variable "deployment_container_endpoint" {
  type = string
}

variable "enabled" {
  default = false
  type    = bool
}

variable "integration_subnet_id" {
  type = string
}

variable "application_insights_connection_string" {
  sensitive = true
  type      = string
}

variable "application_insights_key" {
  sensitive = true
  type      = string
}

variable "allowed_origins" {
  type = list(string)
}

variable "app_settings" {
  type = map(string)
}

variable "tags" {
  type = map(string)
}
