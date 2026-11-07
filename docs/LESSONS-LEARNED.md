# Troubleshooting lessons from the actual platform

These are historical engineering incidents summarized from maintained internal records. They are not newly reproduced tests, a fresh cloud inventory or instructions to repeat a consumed operation. Names, resource identifiers, private payloads and credentials are excluded.

## The API was healthy, but its timers were not

**What happened.** The HTTP health endpoint returned 200 while background listeners failed to start. Repeatedly publishing the API or signing in again would not diagnose that difference.

**What the evidence showed.** The affected host had both managed-identity settings and a nonempty legacy AzureWebJobsStorage connection. Listener failures identified host storage, rather than the business route or a new screening feature, as the failing boundary.

**What changed and how it was checked.** The recorded repair removed only the conflicting plain setting and preserved the managed-identity fields and other application values. Readback, function registration and sampled timer executions then supplied evidence beyond HTTP health.

**What to carry forward.** Separate package publication, HTTP availability, listener startup and completed background work. A successful health request proves only the path it exercised; do not broaden storage permissions or enable account keys to hide a configuration conflict.

Source record: `docs/troubleshooting/release-and-state-reconciliation.md — Production API timer listeners; docs/troubleshooting/stage2-processor-host-storage-authentication.md`. These internal paths identify provenance; they are not public file links.

## Related incident

[Terraform setting preservation](https://github.com/truthofsource/terraform-modules-and-safe-adoption/blob/main/docs/LESSONS-LEARNED.md) explains the shared failure and verification. Its historical acceptance is not another hosted test performed for this repository.

## Evidence and project boundaries

The local examples and screenshots in this repository remain separate from the dated hosted incidents above. A new documentation summary does not establish another successful deployment, restore, security scan or business transaction. Follow the repository’s existing validation guide for the commands and limits of the runnable reference.

The practical sequence is: identify the failing boundary, preserve safe correlation evidence, reconcile any uncertain result, apply only the relevant repair and verify the resulting state. A completed local command is not interchangeable with a completed cloud operation.
