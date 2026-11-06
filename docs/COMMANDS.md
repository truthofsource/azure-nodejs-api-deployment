# Commands and expected results

## Prerequisites

Use Node 22, npm and Python 3.12. Terraform is only needed for infrastructure/mock checks. Docker, Azure login and Core Tools are not required for the default local tests. No command below publishes to Azure.

```bash
npm ci --prefix sample-api --ignore-scripts --no-audit --no-fund
npm test --prefix sample-api
python -B -m unittest discover -s tests -v
python -B -m unittest discover -s reference -v
python -B -m lab demo
```

Expected: three direct-handler tests, seven new package tests, six original diagnostic tests and six demonstration assertions. The SDK's test-mode warning means there is no Functions host; it is not a failed Azure deployment.

PowerShell uses the same commands; use npm.cmd if execution policy intercepts npm.ps1. A Python virtual environment is optional because this example uses the standard library.

## Run the actual Node handler through the local harness

```bash
npm run serve:local --prefix sample-api
curl http://127.0.0.1:8020/api/health
```

The first command keeps running; use another terminal for curl. On PowerShell, use curl.exe or Invoke-RestMethod. Expect status/service/environment/timestamp. This loopback server is a direct-handler harness, not the Azure Functions host. Ctrl+C stops it.

## Run the packaging workbench

```bash
python -B -m lab serve --port 8011
```

Open the loopback dashboard on port 8011. It uses fictional compiled package inputs and the actual packaging/verifier functions, without calling the Node server or Azure.

## Optional real local Functions host — not required or accepted by the default tests

Install compatible Azure Functions Core Tools v4 and the local Azurite storage emulator, then use the sample settings. In PowerShell:

```powershell
Copy-Item sample-api/local.settings.example.json sample-api/local.settings.json
Set-Location sample-api
npm.cmd run build
func start
```

Azurite must be running separately. The example uses local-emulator storage, not a cloud account. local.settings.json stays ignored and must never be packaged. Running this option would establish a different level of acceptance from the direct-handler tests; it was not run for the default screenshot.

## Terraform schema and mock plans

```bash
terraform -chdir=infra init -backend=false -input=false
terraform -chdir=infra fmt -check -recursive
terraform -chdir=infra validate
terraform -chdir=infra test
```

Expected: three mock tests and no resource apply. The default host is Disabled. Example dependencies are placeholders, not a complete cloud environment.
