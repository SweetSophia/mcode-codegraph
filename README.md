# CodeGraph for MiniMax Code

A [MiniMax Code marketplace plugin](https://minimax.io) that wires the
[CodeGraph](https://github.com/colbymchenry/codegraph) pre-indexed code
knowledge graph into MiniMax Code as a stdio MCP server.

One MCP call returns the relevant symbols' verbatim source, the call paths
between them, and a blast-radius summary — so the agent answers structural
questions directly instead of grep+read loops.

## What it does

- Adds `mcp__codegraph__explore` to the MiniMax Code tool surface.
- Lets the agent answer "how does X work", "how does X reach Y", and
  "what's the blast radius of changing X" in one call.
- Per-project indexing (run `codegraph init` once), with native file-watcher
  auto-sync — the graph stays fresh while you code, no manual `sync`.

## Installation

### Through the MiniMax marketplace

This package is the form-ready submission to the
[MiniMax Marketplace](https://vrfi1sk8a0.feishu.cn/share/base/form/shrcnbnpeor3z72fUkeHzrOE7vb).
See [`SUBMISSION.md`](./SUBMISSION.md) for the submission handoff.

### Manual install (dev / local testing)

1. Install the CodeGraph CLI:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh
   # or, with Node available:
   # npm i -g @colbymchenry/codegraph
   ```

2. Copy this package into the MiniMax plugin cache layout, or point your
   local plugin loader at it.

3. Restart MiniMax Code. The MCP tool `mcp__codegraph__explore` will appear.

4. In each project you want indexed, run once:
   ```bash
   codegraph init
   ```

## Requirements

- MiniMax Code (any recent build with the OFFICIAL plugin loader).
- CodeGraph CLI v1.6.0 or newer on `PATH`.
- Node 22.5+ if you use the embedded `@colbymchenry/codegraph` package
  directly (not required for the MCP server, which bundles its own runtime).

## How it works

```
MiniMax Code ──▶ mcp__codegraph__explore ──▶ codegraph serve --mcp
                                                   │
                                                   ▼
                                       SQLite knowledge graph
                                       (symbols · edges · files · FTS5)
```

CodeGraph parses each source file with a native Rust kernel (20 languages,
tree-sitter-validated, byte-identical graphs to the reference engine),
stores nodes and edges in `.codegraph/codegraph.db` (WAL mode), resolves
imports and calls cross-file, and watches the project for changes with a
debounced auto-sync.

## Package contents

| Path | Purpose |
| --- | --- |
| `.minimax-plugin/plugin.json` | MiniMax marketplace manifest |
| `codegraph.mcp.json` | MCP server config (stdio, `codegraph serve --mcp`) |
| `skills/codegraph-mcode/SKILL.md` | Agent guidance for when/how to call the MCP tools |
| `icon.png` | Plugin icon |
| `README.md` | This file |
| `SUBMISSION.md` | MiniMax marketplace submission handoff |

## License

MIT. See upstream [CodeGraph LICENSE](https://github.com/colbymchenry/codegraph/blob/main/LICENSE).