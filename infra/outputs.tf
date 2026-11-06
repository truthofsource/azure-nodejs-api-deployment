output "id" {
  value = azurerm_function_app_flex_consumption.workforce_api.id
}

output "name" {
  value = azurerm_function_app_flex_consumption.workforce_api.name
}

output "default_hostname" {
  value = azurerm_function_app_flex_consumption.workforce_api.default_hostname
}

output "principal_id" {
  value = azurerm_function_app_flex_consumption.workforce_api.identity[0].principal_id
}
