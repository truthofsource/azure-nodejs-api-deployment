# Build and package the Node application

1. npm ci installs the reviewed lockfile. The minimal sample pins @azure/functions 4.16.1, TypeScript 5.9.3 and Node types 22.20.0 from the platform's selected lockfile versions.
2. Production TypeScript compilation excludes *.test.ts. The real output glob is dist/src/functions/*.js, matching package.json main. Changing rootDir/outDir without changing that entrypoint can leave the host with no discoverable Functions.
3. Run handler and release tests before removing development dependencies. The real platform additionally has business/SQL/browser/security suites; the small public sample does not reproduce their full coverage.
4. Prune development dependencies or stage a clean runtime install. Include host.json, package.json, lockfile, compiled code, runtime node_modules and reviewed migrations/templates. Public placeholder directories contain no actual forms/data.
5. The actual packager sorts paths, fixes ZIP timestamps/modes and excludes .bin shims, application test files and source maps. Package root layout matters: host.json belongs at ZIP root, not under sample-api/ or another parent folder.
6. Verify source/digest, safe archive paths, duplicate entries, literal Function names and the allowed commissioning shields before any publication.

The public shield profile contains only health=Disabled. It does not reproduce the private environment's complete route/worker settings. An archive passing this profile is not approved to run on the business platform.

## Local archive reference

From the repository root, after npm test:

```bash
npm prune --prefix sample-api --omit=dev --ignore-scripts --no-audit --no-fund
python -B scripts/package-local.py --source-sha <full-reviewed-40-character-sha>
```

Use a real selected commit when making a real archive. The command only creates .release/release.zip and release.json and verifies them locally; it uploads nothing. Re-run npm ci before compiling again because TypeScript was a development dependency. The receipt alone cannot establish trusted source provenance.

## Linux and native dependencies

The full operational API includes native image-processing dependencies. Node major version alone is insufficient: OS, CPU architecture and libc/binary compatibility matter. Do not promote Windows node_modules into the Linux runtime. Use the appropriate Linux build environment and smoke-test native imports and relevant business paths. The minimal public health sample has no such native image-processing dependency and does not prove their compatibility.

Deterministic ZIP evidence assumes identical file bytes and packaging/compression toolchain. It does not claim Windows and Linux dependency trees are identical.
