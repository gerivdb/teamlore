---
kind: mistake
commit: 586abd9
verify_by: 2026-09-03
paths:
  - src/gateway/**/*
  - tools/ecos-cli/**/*
---
# Oublier de fermer le clapet BDCP avant push

Le clapet BDCP doit être fermé avant tout `git push`.
Sortir en mode FREE consomme le quota Antigravity de l'utilisateur.
