---
name: skl-009-lore-injection
description: Lore Injection Skill — Path-scoped recall injection for teamlore. Injects relevant lore entries into agent context based on file paths being edited. Implements path-scoped recall per ADR-2026-08-03-001.
---

# SKL-009 — Lore Injection Skill

## Purpose

Inject relevant teamlore entries into agent context based on the file paths being edited. Implements **path-scoped recall** per ADR-2026-08-03-001 (teamlore Lore-as-Code).

## When to Use

- Agent starts working on files in a repo with existing lore
- Pre-commit hook triggers context injection
- Agent explicitly requests lore for current working directory
- CI/CD pipeline validates lore injection coverage

## Injection Algorithm

`
1. Identify current working file paths (globs)
2. Query .lore/ for entries matching those paths
3. Filter by kind (mistake > gotcha > decision priority)
4. Inject top-N entries (token budget ~800 tokens)
5. Annotate with kind, commit, verify_by
`

## Entrypoints

### 	eamlore inject <path> [--budget <tokens>]

Injects relevant lore for the given path(s).

`ash
teamlore inject src/reducer.zig --budget 800
`

### 	eamlore inject --changed

Injects lore for files changed in the current git diff.

### 	eamlore inject --all

Injects all lore for the current repository.

## Output Format

Injected lore entries are formatted as:

`
=== LORE INJECTION (path: src/reducer.zig) ===
[mistake] bdcp-clapet.md (commit: a1b2c3d4, verify_by: 2026-08-15)
  Never call POST /clapet/open without explicit user instruction.
  BDCP mode is inviolable — protects token quota and network anonymity.
  Paths: src/gateway/clapet.rs, scripts/bdcp_guard.sh

[gotcha] zig-015-api.md (commit: e5f6g7h8, verify_by: 2026-07-20)
  Zig 0.15 changed std.time.sleep() -> std.os.windows.kernel32.Sleep()
  Paths: src/*.zig, build.zig
=== END INJECTION ===
`

## Configuration

- **Budget**: Default 800 tokens, max 2000 tokens
- **Priority**: mistake > gotcha > decision
- **Max entries**: 10 per injection
- **Recency bias**: Entries with verify_by > 30 days ago get lower weight

## Integration Points

- **Pre-commit hook**: .githooks/pre-commit calls teamlore inject --changed
- **CTULU**: Orchestrates injection in agent sessions
- **KORX**: Stores compressed lore entries in .kbin format
- **SPIDX**: Uses lore graph for causal rewriting

## Anti-Patterns

| Anti-Pattern | Consequence |
|-------------|-------------|
| Injecting all lore (>2000 tokens) | Context overflow, agent confusion |
| Ignoring verify_by date | Stale guidance injected |
| Injecting for wrong paths | Irrelevant noise, reduced signal |
| Skipping verification | Stale/incorrect guidance persists |

## References

- ADR-2026-08-03-001-TEAMLORE-LORE-AS-CODE
- Source 52: teamlore — Break things only once
- IntentHash: 0xSKL_009_LORE_INJECTION_20260803
