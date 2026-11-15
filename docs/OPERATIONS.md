# Troubleshooting a Node API release

**Terms used here:** An artifact is a file produced for a release, such as an application ZIP or container image. DNS turns a service name into the network address used to reach it.

| Symptom | Likely investigation | Safe next step |
| --- | --- | --- |
| No Functions found | package main glob, dist root, app.http imports/registrations, build output | Inspect the ZIP root and compiled entrypoint paths before publishing again |
| SDK says test mode locally | Direct node execution outside the Functions host | Treat handler tests separately; use Core Tools only for a separately prepared host check |
| Module not found on Linux | Runtime dependencies pruned incorrectly, wrong path or native OS/ABI mismatch | Rebuild runtime staging for the actual Linux target; do not upload Windows node_modules |
| Deployment storage denied | Identity, role scope or storage route/configuration | Read back the correct deployment identity/container; identity assignment alone grants nothing |
| Health 200 but business path fails | Entra audience/role, current staff state, SQL/Blob permission, private DNS or dependent job | Test each business dependency under authorized fictional acceptance |
| API appears unavailable | Runtime may be intentionally Disabled or a Function shield may be Off | Check current intended operating state before starting anything |
| Artifact hash differs | Wrong selected bytes or host repackaging | Verify trusted archive first; use explicit file/tree diagnostic policy when appropriate |
| Timer/worker runs after release | Runtime settings or package boundaries changed | Preserve evidence, contain the owned worker and reconcile settings; code publication is not activation |

Do not log bearer tokens, raw app-setting dumps, employee data or secret-bearing URLs. The public health endpoint is not a token transport; send no sensitive query parameters. Keep errors tied to stage and safe correlation evidence.

The actual archive verifier and diagnostic helper do not replace dependency/image scanning, authorization checks or production approval. Six green package checks are not evidence that all platform vulnerabilities are fixed.
