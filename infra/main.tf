resource "azurerm_function_app_flex_consumption" "workforce_api" {

  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location

  service_plan_id = var.service_plan_id

  storage_container_type      = "blobContainer"
  storage_container_endpoint  = var.deployment_container_endpoint
  storage_authentication_type = "SystemAssignedIdentity"

  runtime_name    = "node"
  runtime_version = "22"

  maximum_instance_count = 10
  instance_memory_in_mb  = 2048

  # Runtime enablement and containment gates remain owned by the environment root.
  enabled = var.enabled

  https_only                                     = true
  webdeploy_publish_basic_authentication_enabled = false
  virtual_network_subnet_id                      = var.integration_subnet_id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    application_insights_connection_string = var.application_insights_connection_string
    application_insights_key               = var.application_insights_key

    cors {
      allowed_origins = var.allowed_origins

      support_credentials = false
    }
  }

  app_settings = var.app_settings


  tags = var.tags
}
