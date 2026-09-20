# MiniMax Marketplace Submission

This file is the owner handoff for the MiniMax Marketplace form. It is not a
runtime instruction and contains no credentials.

## Package

- Plugin name: `mcode-codegraph`
- Package version: `0.1.0`
- Source: `https://github.com/SweetSophia/mcode-codegraph`
- Manifest: `.minimax-plugin/plugin.json`
- Operation: `New plugin` until the first submission passes validation.

A validation failure does not create an existing Marketplace plugin. Retry a
rejected first submission as `New plugin`; use `Update` only after MiniMax
has accepted an earlier submission and established the listing.

## Requested catalog placement

- Target regions: `US` (and `CN` if the runtime is available there)
- Delivery targets: `Desktop` first; `Cloud` only after the App/Connector
  rollout confirms the provider contract — this package has no App surface
  today.
- Organization: `SweetSophia`
- Contact: use the owner's submission address at form time; do not commit
  it here.

The package is mechanically ready for Desktop. The Cloud target is
intentionally not requested at this version — there is no App/Connector
to gate. Revisit when a managed connection story is in scope.

## What this package contains

| Capability | Status | Notes |
| --- | --- | --- |
| Skill | yes | `skills/codegraph-mcode/SKILL.md` |
| stdio MCP | yes | `codegraph.mcp.json` — `codegraph serve --mcp` |
| streamable-http MCP | no | not used |
| Apps | none | `apps: []` in the manifest |
| Hooks | none | — |

## Review checklist

- [x] `.minimax-plugin/plugin.json` is at the package root.
- [x] The package contains Skill and stdio MCP capabilities.
- [x] The MCP server launches a locally installed CLI (`codegraph`) — no
      embedded binary, no install script, no symlink, no native build, no
      secret, no personal data.
- [x] The MCP command (`codegraph serve --mcp`) is on `PATH` from the
      user's installation. The package does not bundle or vendor it.
- [x] The Skill does not claim automatic transcript capture or lifecycle
      hooks.
- [x] Telemetry is opt-in (CodeGraph's anonymous aggregated pipeline) and
      can be disabled by the user at any time.
- [ ] Owner submits the form and retains the submission ID.
- [ ] Owner checks the submission status using the original Feishu account
      and submission email.

## Form

Submit through the official MiniMax form:

`https://vrfi1sk8a0.feishu.cn/share/base/form/shrcnbnpeor3z72fUkeHzrOE7vb`

Use the exact package name from `.minimax-plugin/plugin.json`. For the
GitHub source, select the repository and provide the `main` ref.

## After MiniMax confirms

1. Add the catalog entry under the approved regions.
2. Bump `version` in `.minimax-plugin/plugin.json` to a `-market.1` suffix
   for the first published build, then keep semver for follow-ups.
3. Re-run package validation and publish a new version before requesting
   any update review.