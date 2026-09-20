---
name: codegraph-mcode
description: Use the CodeGraph MCP server (mcp__codegraph__*) instead of grep+read loops when answering structural questions about the current project.
---

# CodeGraph for MiniMax Code

## When to reach for it

Use `mcp__codegraph__explore` (or any other `mcp__codegraph__*` tool when explicitly enabled) for almost any structural question:

- "How does X work?"
- "How does X reach Y?" — a flow or call-path question
- A survey of an area of the code
- "What's the blast radius if I change X?"

The MCP server ships its own usage guidance via `initialize`, which steers you to answer directly rather than delegate to file-reading sub-agents.

## When NOT to use it

- The project has no `.codegraph/` yet — run `codegraph init` first, then come back.
- The question is purely textual (e.g. "what does this error string say?") — read the file directly.
- A file the question hinges on is unindexed. After edits, wait ~2s for the debounced auto-sync; the response banner will name any stale file and tell you to `Read` it directly.

## One-time setup per project

In the project directory:

```
codegraph init
```

This builds `.codegraph/codegraph.db` and starts a native file watcher. Every save auto-syncs in ~2s. The graph stays fresh — no manual `codegraph sync` is needed in normal use.

## Tool surface

| Tool | Visible by default | Purpose |
| --- | --- | --- |
| `mcp__codegraph__explore` | yes | One call → relevant symbols' source + call paths + blast radius. The workhorse. |
| `mcp__codegraph__node` | no | One symbol's source + caller/callee trail. |
| `mcp__codegraph__search` / `mcp__codegraph__query` | no | FTS5-backed symbol search. |
| `mcp__codegraph__callers` / `mcp__codegraph__callees` | no | Caller/callee edges for a symbol. |
| `mcp__codegraph__impact` | no | Blast-radius for a symbol at a given depth. |
| `mcp__codegraph__files` | no | Project file tree from the index. |
| `mcp__codegraph__status` | no | Index health check. |

Re-enable the hidden tools by setting `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status` on the MCP server in `codegraph.mcp.json`.

## Multi-project sessions

The MCP tool accepts `projectPath` so a monorepo where only some services are indexed, or a second repo, works in one session. A path with no `.codegraph/` returns clean guidance to use built-in tools instead — nothing fails loudly.

## Operational notes

- The MCP server uses `node:sqlite` (bundled) in WAL mode. Reads never block on writes.
- One writer per project (the shared background daemon or a single direct-mode process). If `codegraph status` ever shows the watcher stopped, run `codegraph daemon` and pick it up again.
- Telemetry is anonymous and aggregated locally before send. Turn it off any time with `codegraph telemetry off`, `CODEGRAPH_TELEMETRY=0`, or `DO_NOT_TRACK=1`.

## References

- Upstream: https://github.com/colbymchenry/codegraph
- Docs: https://colbymchenry.github.io/codegraph/
- `codegraph --help` and `codegraph <command> --help` for the CLI surface.