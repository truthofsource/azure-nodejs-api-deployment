# Validation — November 6, 2026

| Executed local check | Result |
| --- | --- |
| Minimal TypeScript API compilation | Passed; TypeScript 5.9.3, Node 22.23.2 |
| Actual health-handler tests | 3 passed; @azure/functions 4.16.1 SDK test mode |
| New actual-packager fixture tests | 7 passed |
| Original selected ZIP diagnostic tests | 6 passed |
| Direct Node HTTP harness | Health 200; missing route 404, POST 405 and wrong Host 403 |
| Compiled sample runtime-only package | Created/pruned/verified locally; no upload |
| Demonstration assertions | 6 passed with fictional package inputs |
| Terraform schema / mock plans | Valid; 3 passed; no apply; signed azurerm 4.81.0 lockfile |
| Desktop/mobile UI | Passed at 1440/390 px; no overflow or runtime errors |
| Loopback boundaries | External-Origin write denied; unlisted asset denied |
| Workflow syntax | actionlint 1.7.12 passed; manual-only; no hosted run |

The [machine record](validation-results.json) records date, versions and source hashes. Screenshots show actual local package code with fictional inputs. The separately compiled handler was exercised through both direct tests and the Node HTTP harness.

The local actual sample archive uses a fictional a*40 source label to exercise the packager; that is not trusted commit/source attestation. It contains the actual compiled minimal health handler and production dependencies, not the complete business API. Installed dependencies and archive bytes remain local and ignored.

SDK test mode means the Azure Functions host was not started. The direct HTTP harness is not Core Tools or hosted trigger discovery. No Linux acceptance of the full platform's native dependencies is claimed. A live release still needs its real source/lockfile, Linux runtime packaging, trusted artifact/archive evidence, appropriate roles/routes, hosted health and protected business-path checks.

No Azure query, upload, app/scanner/worker activation, role grant or business operation occurred. The public workflow was not dispatched and uploads no artifact.

Reproduce with [the commands](COMMANDS.md) and [source map](SOURCE-MAP.md).
