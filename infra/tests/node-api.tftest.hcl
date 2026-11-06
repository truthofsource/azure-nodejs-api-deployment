mock_provider "azurerm" {}
variables {
  subscription_id                        = "00000000-0000-4000-8000-000000000001"
  name                                   = "func-example-node-api"
  resource_group_name                    = "rg-example-app"
  location                               = "eastus2"
  service_plan_id                        = "/subscriptions/00000000-0000-4000-8000-000000000001/resourceGroups/rg-example-app/providers/Microsoft.Web/serverFarms/plan-example-flex"
  deployment_container_endpoint          = "https://exampledeployment.blob.core.windows.net/function-releases"
  integration_subnet_id                  = "/subscriptions/00000000-0000-4000-8000-000000000001/resourceGroups/rg-example-network/providers/Microsoft.Network/virtualNetworks/vnet-example/subnets/functions"
  application_insights_connection_string = "InstrumentationKey=00000000-0000-4000-8000-000000000002"
  application_insights_key               = "00000000-0000-4000-8000-000000000002"
  allowed_origins                        = ["https://portal.example.invalid"]
  app_settings                           = { "WORKFORCE_ENVIRONMENT" = "nonproduction", "AzureWebJobs.health.Disabled" = "true" }
  tags                                   = { environment = "reference" }
}
run "node_runtime_and_default_pause" {
  command = plan
  assert {
    condition     = azurerm_function_app_flex_consumption.workforce_api.runtime_name == "node" && azurerm_function_app_flex_consumption.workforce_api.runtime_version == "22" && azurerm_function_app_flex_consumption.workforce_api.enabled == false
    error_message = "Preserve Node 22 and a default-paused example."
  }
}
run "identity_storage_and_https_boundary" {
  command = plan
  assert {
    condition     = azurerm_function_app_flex_consumption.workforce_api.storage_authentication_type == "SystemAssignedIdentity" && azurerm_function_app_flex_consumption.workforce_api.identity[0].type == "SystemAssigned" && azurerm_function_app_flex_consumption.workforce_api.https_only && !azurerm_function_app_flex_consumption.workforce_api.webdeploy_publish_basic_authentication_enabled
    error_message = "Preserve identity-based deployment storage, HTTPS and basic-publish auth Off."
  }
}
run "outbound_network_and_scale_limits" {
  command = plan
  assert {
    condition     = azurerm_function_app_flex_consumption.workforce_api.virtual_network_subnet_id == var.integration_subnet_id && azurerm_function_app_flex_consumption.workforce_api.maximum_instance_count == 10 && azurerm_function_app_flex_consumption.workforce_api.instance_memory_in_mb == 2048
    error_message = "Preserve the selected outbound VNet integration and scale settings."
  }
}
