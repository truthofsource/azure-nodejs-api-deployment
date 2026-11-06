# Scaling, costs, strengths and tradeoffs

**Terms used here:** An artifact is a file produced for a release, such as an application ZIP or container image. Role-based access control gives people or services permissions according to their roles.

| Design | Strength | Tradeoff | Growth response |
| --- | --- | --- | --- |
| Node event loop | Efficient I/O-oriented request handling | CPU-heavy synchronous work can block the loop | Measure event-loop lag; separate CPU-heavy jobs and bound work |
| Flex Consumption | Event-driven Linux runtime with outbound VNet integration | Cold starts, host limits and downstream capacity still matter | Measure actual concurrency/latency before increasing limits |
| Ten instances / 2048 MiB | Explicit selected host bounds | Not a throughput guarantee or spending cap | Consider DB pools, key-service requests, queue claims and provider quotas together |
| Build once / promote selected package | Clear source/artifact trace | Large node_modules/native assets increase build/package size | Stage runtime-only dependencies and validate native imports on the target |
| Identity-based deployment storage | Avoids storing a deployment account key in source | Identity, RBAC, networking and bootstrapping are separate dependencies | Verify exact scopes and readback without broad fallback credentials |
| Separate worker/API packages | Limits privileged and background execution | More artifacts/configuration to maintain | Keep one explicit deployment/activation owner per package |

Functions programming model v4, Functions host version and Node major version are three different version concepts. The selected application uses Node 22 and the v4 SDK model; do not infer a Node upgrade solely from the SDK package number.

The version "2.0" in host.json is the configuration schema value; it does not mean this application runs Azure Functions host v2.

Plan for reusable database connections, timeouts and bounded retries. Adding instances can multiply connection pools and downstream load. Logging/retention, deployment storage, executions and always-ready configuration can affect costs; the public module does not establish a monthly cap. No resource is activated or billed by its local validation.

The full API's image-processing/PDF work may need different memory/concurrency choices from this tiny health sample. This repository does not benchmark production traffic or claim high availability from a local response time.
