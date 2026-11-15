# Build your own from scratch: Azure Nodejs Api Deployment

Your own JavaScript Azure Function, tested locally and published to a new Function App.

Start with a new folder, your own files and your own accounts. The numbered steps below describe the build; no portfolio repository checkout is required. The existing implementation/evidence elsewhere in this repository is a separate reference, not a claim that your new build has already passed.

## Prerequisites

Supported Node LTS, Azure Functions Core Tools v4, Azurite for local host storage, Azure CLI, and an Azure subscription with a budget and permission to create a new Function App/storage account.

Use Bash on Linux/macOS/WSL for Bash blocks and PowerShell for PowerShell blocks. Select the tool versions supported by the official sources below, record the versions you actually install and retain generated dependency locks. Cloud resources, scanner downloads, logs and external AI calls can create costs; review the stated scope before enabling them.

## Create your project folder

Choose a new folder name. These first commands create a blank project; an optional `git init` gives it its own history. Create parent directories in your editor when a later step introduces a nested file.

```bash
mkdir my-azure-nodejs-api-deployment
cd my-azure-nodejs-api-deployment
git init
```

Create `.gitignore` before saving credentials or build outputs:

```gitignore
.venv/
node_modules/
.env
.env.*
local.settings.json
credentials.json
token.json
*.pem
*.key
*.tfstate*
*.tfplan
.terraform/
private*/
captures/
backups/
batch.json
reports/
out/
app-config.local.yaml
```

The source/file snippets are a starting implementation you type or paste into the named files. Replace `YOUR_*`, names, regions and addresses only with values from your own lab; do not place real client/employee records in a test project. Keep your terminal in this project root unless a step explicitly changes directory.

Before a first commit, set your own repository-local author with `git config user.name "YOUR_NAME"` and `git config user.email "YOUR_PUBLIC_COMMIT_EMAIL"`. Review `git status --short` and the staged diff before publishing; ignored local files are not a substitute for reviewing what you upload.

## Step 1 — Generate a new Functions project

**Where:** Your empty project folder.

Use Core Tools to generate a JavaScript project and an HTTP-trigger template named health. This generator creates your own app; it does not check out the portfolio repository.

```bash
func init . --worker-runtime node --language javascript
func new --template "HTTP trigger" --name health --authlevel anonymous
```

**Check before continuing:** The folder contains host.json, package.json and a health function file.

## Step 2 — Write the health handler

**Where:** The generated function file under src/functions.

Replace the generated HTTP function with the code below and confirm package.json main includes that directory. Keep the response limited to service health; never expose environment variables, tokens or database strings.

Create **`src/functions/health.js`** with the following contents:

```javascript
const { app } = require('@azure/functions');
app.http('health', {
  methods: ['GET'], authLevel: 'anonymous',
  handler: async () => ({jsonBody: {service: 'my-api', status: 'ok'}})
});
```

**Check before continuing:** The function registers GET health through the v4 app model.

## Step 3 — Run your local host

**Where:** Two workstation terminals.

Start Azurite in a separate terminal and confirm the ignored local.settings.json uses your local emulator connection. Run func start, then request /api/health on the port printed by Core Tools.

```bash
npm install
func start
# In a second terminal:
curl -i http://localhost:7071/api/health
```

**Check before continuing:** A real Functions host returns your JSON; local settings are excluded from Git.

## Step 4 — Create the Azure host

**Where:** Azure Portal → Function App → Create.

Create a new Linux Function App using a currently supported Node runtime and hosting plan in your isolated group. Choose its storage account, monitoring workspace and identity deliberately; inspect the estimated plan/storage/log costs and network reachability requirements.

**Check before continuing:** The app exists with the selected runtime and reachable host-storage dependencies.

## Step 5 — Publish the project you created

**Where:** Your project folder.

Select your intended subscription and publish only to the newly named Function App. Confirm that the package excludes local.settings.json and that required app settings are configured on the host.

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
func azure functionapp publish YOUR_FUNCTION_APP_NAME
```

**Check before continuing:** The publish completes and your hosted /api/health route returns the expected JSON.

## Step 6 — Add the identity boundary and verify it

**Where:** Function App → Authentication.

For staff endpoints, configure Microsoft Entra authentication, the correct audience and restricted user/app access before exposing business data. Test both authorized and unauthenticated calls; function keys, Entra identity and employee ownership are different controls.

**Check before continuing:** You have a health check plus separately recorded access tests, not a claim that health proves all APIs work.

## Step 7 — Capture the release and close the lab

**Where:** Your files and Azure Portal.

Record the runtime, package source, deployment outcome, health response and authentication results. Delete only this dedicated lab group after reviewing retained monitoring/storage costs.

**Check before continuing:** Your own app can be rebuilt from its files and deployment notes.

## Verification and your own screenshots

| Evidence | What to record | Your result |
| --- | --- | --- |
| New build | Your own files/resource settings and tool versions | Not yet recorded |
| Working path | The actual successful request, configuration or recovery result | Not yet recorded |
| Failure boundary | A meaningful denied, malformed, stale or failed case | Not yet recorded |
| Recovery / cleanup | What you restored or removed and what remains billed | Not yet recorded |

Capture your own architecture/configuration, one working result and one failure/recovery result. Keep tokens, credentials, personal records and private identifiers out of public screenshots. Existing portfolio images are references, not evidence that you performed these steps.

## Troubleshooting order

1. Confirm the named file, working directory and selected tool/interpreter.
2. Check the exact input and resource/account selected for the failing step.
3. Separate identity permission, network/DNS reachability and application validation.
4. Keep the actual error and reconcile an unknown write outcome before repeating it; do not widen access or repeat paid operations blindly.

The numbered steps describe a build procedure. Local syntax checks, an accepted API request, a completed hosted operation and a human verification are different evidence levels; fill in the verification table with what you actually observed.

## Official implementation references

- [learn.microsoft.com — create-first-function-cli-node](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-node)
- [learn.microsoft.com — functions-reference-node](https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-node)

The walkthrough layout follows the prerequisites → creation/configuration → test → verification → troubleshooting → cleanup pattern of the [Splunk project reference](https://github.com/davidharris6/splunk-siem-log-analysis). Its Splunk-specific settings are not copied into unrelated projects.
