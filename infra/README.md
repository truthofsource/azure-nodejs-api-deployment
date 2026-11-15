# Actual Flex host module, standalone reference

This is the actual nonproduction API host module with neutral resource labels, public provider configuration and enabled=false as a new safe default. The original environment-specific lifecycle ignore rules for operator-owned storage/SMS settings are omitted because this standalone sample owns no such live settings. Do not use this public root to reconcile the existing platform.

The source declares Node 22, 2048 MiB, maximum ten instances, system-assigned identity, identity-based deployment-container access, outbound VNet integration, HTTPS and basic publishing authentication Off. App Insights/CORS/settings are inputs. They do not establish live log arrival, authorization or successful storage access.

Provide an existing reviewed Flex plan, deployment container, integration subnet and monitoring configuration before a separate real apply. Commission exact identity/storage roles and host-storage settings separately. No plan, storage account, DNS, role grant, SQL or publishing workflow is created here. VNet integration is outbound and CORS is not authentication.

```bash
terraform -chdir=infra init -backend=false -input=false
terraform -chdir=infra validate
terraform -chdir=infra test
```

Three tests using simulated cloud responses inspect runtime/pause, identity/HTTPS and network/scale values. The selected provider version is retained in the signed lockfile. Mock plans do not access Azure or prove that the example inputs can be commissioned. Real settings, secrets, plans and state remain private.
