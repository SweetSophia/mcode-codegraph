import json
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    manifest_path = ROOT / ".minimax-plugin" / "plugin.json"
    mcp_path = ROOT / "codegraph.mcp.json"
    readme_path = ROOT / "README.md"
    submission_path = ROOT / "SUBMISSION.md"
    skill_path = ROOT / "skills" / "codegraph-mcode" / "SKILL.md"
    icon_path = ROOT / "icon.png"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
    readme = readme_path.read_text(encoding="utf-8")
    submission = submission_path.read_text(encoding="utf-8")
    skill = skill_path.read_text(encoding="utf-8")

    # manifest invariants
    assert manifest["name"] == "mcode-codegraph"
    assert manifest["displayName"] == "CodeGraph for MiniMax Code"
    assert manifest["version"] == "0.1.0"
    assert manifest["icon"] == "icon.png"
    assert manifest["category"] == "Code"

    example_queries = manifest["exampleQueries"]
    assert 0 <= len(example_queries) <= 3, f"got {len(example_queries)} example queries"
    assert all(
        isinstance(q, str) and q.strip() and len(q) <= 4_096
        for q in example_queries
    ), "every example query must be a non-empty string ≤ 4096 chars"

    assert manifest["mcpServers"] == ["codegraph.mcp.json"]
    assert manifest["skills"] == ["skills/codegraph-mcode/SKILL.md"]

    # MCP server shape — stdio, launching the locally installed CLI
    server = mcp["mcpServers"]["codegraph"]
    assert server["type"] == "stdio"
    assert server["command"] == "codegraph"
    assert server["args"] == ["serve", "--mcp"]
    assert "timeout" in server and server["timeout"] >= 30_000
    assert "description" in server and server["description"]

    # icon exists and is a real PNG
    assert icon_path.exists(), "icon.png missing"
    head = icon_path.read_bytes()[:8]
    assert head.startswith(b"\x89PNG\r\n\x1a\n"), "icon.png is not a valid PNG"

    # skill does not overclaim — no transcript capture, no lifecycle hooks
    assert "do not claim automatic transcript capture" not in skill.lower()
    assert "lifecycle hook" not in skill.lower()

    # README and SUBMISSION point at the MiniMax marketplace form
    assert (
        "vrfi1sk8a0.feishu.cn/share/base/form" in readme
        or "vrfi1sk8a0.feishu.cn/share/base/form" in submission
    ), "MiniMax marketplace submission link missing from SUBMISSION.md"

    # no file in the package is executable (matches the marketplace rule:
    # no install script, executable, or symlink in the package)
    execute_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    for path in ROOT.rglob("*"):
        if path.is_file():
            assert not (path.stat().st_mode & execute_mask), path

    print("minimax plugin package: PASS")


if __name__ == "__main__":
    main()