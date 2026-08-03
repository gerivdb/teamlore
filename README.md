# teamlore - Mémoire Partagée Souveraine

**IntentHash** : `0xTEAMLORE_LORE_AS_CODE_20260803`
**Version** : 0.1.0
**Layer** : L4-TOOLS
**Philosophy** : "Break things only once"

## Description

`teamlore` est le système de **mémoire partagée souveraine** de l'écosystème `gerivdb`. Il capture les erreurs, décisions d'architecture et "gotchas" techniques dans des fichiers de lore compacts, stockés dans `.lore/`.

## Concepts Clés

### Lore-as-Code
Le savoir est traité comme du code :
- **Proposé par l'agent** après une correction ou décision
- **Revu et mergé par un humain** via Pull Request
- **Stocké dans Git** pour synchronisation instantanée

### Path-Scoped Recall
L'injection de contexte est **sélective et chirurgicale** :
- L'agent ne charge que le lore correspondant aux fichiers modifiés
- Empreinte limitée à ~800 tokens
- Filtres par globs de chemins

### Typologie du Lore

| Kind | Description | Exemple |
|------|-------------|---------|
| `mistake` | Erreur corrigée | "Oublier de fermer le clapet BDCP avant push" |
| `gotcha` | Piège technique subtil | "Zig 0.15 sleep() nécessite kernel32.Sleep() sur Windows" |
| `decision` | Choix architectural avec raisonnement | "BDCP mode par défaut pour protéger le quota Antigravity" |

### Structure d'un fichier Lore

```yaml
---
kind: mistake
commit: abc1234
verify_by: 2026-09-01
paths:
  - src/gateway/**/*
  - tools/ecos-cli/**/*
---
# Oublier de fermer le clapet BDCP avant push

Le clapet BDCP doit être fermé avant tout `git push`.
Sortir en mode FREE consomme le quota Antigravity de l'utilisateur.
```

## Commandes

```bash
# Initialiser teamlore dans un repo
teamlore init

# Ajouter une entrée de lore
teamlore add --kind mistake --paths "src/payments/**/*" "Oublier de valider le hash avant commit"

# Valider les entrées de lore
teamlore validate .lore/

# Générer la scarmap
teamlore scarmap --output scar-map.html
```

## Intégrations

| Repo | Intégration |
|------|-------------|
| KORX | Stockage `.kbin` des états de lore compressés |
| SPIDX | Graphe de force pour la scarmap |
| TALEX | Intégration des cicatrices dans la génération narrative |
| VERSES | Enrichissement des personas avec contexte lore |
| CTULU | Orchestration de l'injection path-scoped |

## Architecture

```
teamlore/
  README.md               # Ce fichier
  .lore/                  # Racine des fichiers de lore
    <repo>/
      <path>/
        <slug>.md         # <= 120 mots
  SCAR-MAP/               # Cartes SVG/HTML générées
  skills/                 # Skills d'injection/validation
  citizens/               # Citizens de gestion du lore
```

## Licence

MIT - Écosystème gerivdb
