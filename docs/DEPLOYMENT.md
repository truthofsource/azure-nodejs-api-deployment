# Controlled Flex publication and promotion

**Terms used here:** An artifact is a file produced for a release, such as an application ZIP or container image. A managed identity lets an Azure service request access without storing a password in the application.

The real release path builds and verifies API archives, publishes into a bounded nonproduction window, records the selected release file and promotes the verified package. Publication and runtime activation are separate decisions: preserve switches, identities, bindings and original power states. Do not enable background jobs just because new code exists.

Flex Consumption has its own supported package-deployment mechanism. Do not assume legacy ZIP deploy, arbitrary external run-from-package URLs, FTP or every App Service deployment recipe applies. The artifact can still be a ZIP without using the legacy ZIP-deploy technology. [Microsoft deployment matrix](https://learn.microsoft.com/en-us/azure/azure-functions/functions-deployment-technologies)

Deployment-storage managed identity needs the required container/account access and a working path. Runtime host storage and downstream resources have their own grants/settings. Deployment OIDC identity is separate from the running Function identity; the public workflow uses neither and cannot publish to Azure.

The source verifier requires every Function registration to match an explicit commissioning profile. The API and privileged directory worker are separate packages/hosts. A literal registration name, unique entry and explicit shield prevent unexpected Functions from being silently treated as approved.

## Same artifact versus repackaged runtime content

Promote the selected retained artifact, not a rebuild. If the hosting platform repackages the active content, raw ZIP equality and filesystem equality are different checks. The actual diagnostic helper compares file hashes and directory trees, rejects unsafe/duplicate entries and emits hashed/aggregate evidence. Content-equivalence acceptance requires the explicit reviewed policy; a random different ZIP is not automatically safe.

## Rollback

Restore a retained compatible package through the reviewed publisher rather than rebuilding an old branch. SQL schema and external operations do not roll back automatically with Node code. [Artifact rollback case study](https://github.com/truthofsource/secure-container-delivery-and-rollback).

This project performs no cloud release, app restart, role grant or production activation. A fresh real deployment needs its own exact release file/source checks and runtime acceptance.
