# Source map and deliberate public adaptations

**Terms used here:** A fixture is test data or a test setup used instead of real business records.

| Public source | Relationship |
| --- | --- |
| sample-api/src/functions/health.ts | Actual handler; neutral service/environment labels |
| sample-api/host.json | Actual host logging/queue extension configuration |
| sample-api/tsconfig*.json | Actual compiled-output and production-test exclusion shape |
| sample-api/package.json | Minimal public dependency set using the selected locked SDK/compiler/type versions, not the full business package |
| reference/release_package.py | Actual package/verify/sha/require functions; Azure clients/publisher/CLI omitted; health-only isolation fixture substituted |
| reference/package_diagnostics.py | Actual ZIP filesystem/hash diagnostic helper |
| reference/test_package_diagnostics.py | Six original selected tests with portable imports |
| reference/content_guard.py | Actual reviewed-filesystem acceptance predicate |
| infra/*.tf | Actual host-module source with neutral labels; standalone provider, enabled=false default and live-settings ignore rules omitted |
| scripts/package-local.py, local HTTP harness, tests/test_packaging.py | Newly authored public wrappers/fixtures; not deployed platform automation |

[Machine source hashes](source-map.json) identify original inputs without publishing private history or identifying configuration. Migration/template folders contain only public README placeholders, not real employee forms or migration history.

The health handler is intentionally public and does not demonstrate business-route authorization. The complete running-portal route allowlist and private commissioning settings are not copied. A passing public package check does not approve a production release.
