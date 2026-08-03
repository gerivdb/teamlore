---
name: skl-010-lore-validation
description: Lore Validation Skill — Validates teamlore entries against schema. Checks frontmatter, word count, path existence, and kind validity. Wraps lore_validator.py with skill interface.
---

# SKL-010 — Lore Validation Skill

## Purpose

Validate teamlore entries against the schema defined in ADR-2026-08-03-001:
- Frontmatter: kind, commit, verify_by
- Word count <= 120
- Paths exist in repo
- Kind validity (mistake, gotcha, decision)

## When to Use

- Pre-commit hook validates staged lore files
- CI/CD pipeline validates all lore entries
- Agent creates new lore entry
- Lore migration/audit

## Entrypoints

### 	eamlore validate <lore-root>

Validates all lore entries under the given root.

`ash
teamlore validate .lore/
`

### 	eamlore validate --file <path>

Validates a single lore file.

`ash
teamlore validate --file .lore/gerivdb/gateway/bdcp-clapet.md
`

### 	eamlore validate --strict

Enforces stricter rules (e.g., verify_by <= 30 days).

## Validation Rules

| Rule | Severity |
|------|----------|
| Frontmatter present | ERROR |
| Required fields: kind, commit, verify_by | ERROR |
| kind in {mistake, gotcha, decision} | ERROR |
| Word count <= 120 | ERROR |
| Paths exist in repo | WARNING |
| verify_by <= 30 days (strict) | WARNING |

## Output Format

`
VALIDATION FAILED
  .lore/gerivdb/gateway/bad-entry.md:
    - missing field: verify_by
    - word count 145 > 120

VALIDATION PASSED
`

## Integration Points

- **Pre-commit hook**: .githooks/pre-commit calls teamlore validate --changed
- **CI/CD**: GitHub Actions runs teamlore validate .lore/
- **CTULU**: Validates before lore injection

## References

- ADR-2026-08-03-001-TEAMLORE-LORE-AS-CODE
- Source 52: teamlore — Break things only once
- IntentHash: 0xSKL_010_LORE_VALIDATION_20260803
