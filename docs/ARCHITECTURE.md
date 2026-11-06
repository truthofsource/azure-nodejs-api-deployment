# Node.js API deployment architecture

The actual application uses the Node.js Azure Functions v4 programming model: app.http and other trigger registrations in code, with package.json pointing to compiled JavaScript. It is distinct from file-based v3 function.json samples and from deploying an Express process into a generic App Service.

The selected host is Flex Consumption with Node 22. Its deployment content is in a configured Blob container authenticated through system-assigned identity. Storage role grants, the Flex plan, host-storage settings and network prerequisites live outside the extracted host module; assigning an identity alone does not grant storage access.

Outbound VNet integration allows approved private downstream paths; it does not close the inbound public HTTP surface. CORS is not authorization. The minimal sample contains only the public health route. Real business handlers verify Entra access tokens and then role/current-state/record access. See [the identity project](https://github.com/truthofsource/cloud-identity-access-automation).

Application Insights host configuration, logging and queue settings come from the real source. A configured destination is not evidence that a particular log arrived. Health 200 does not prove SQL, Blob, signing, provider access or a successful business transaction.

The local UI runs the extracted packager on fictional files. The Node sample separately compiles/invokes the actual handler. The direct HTTP harness is a public reference utility, not Azure Functions Core Tools or hosted-runtime acceptance.
