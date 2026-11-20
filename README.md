# golfo-agent-profiles

Pack oficial de contenido de [agent-ready-setup](https://github.com/guidomodarelli/golfo-marketplace/tree/main/plugins/golfo-agent-ready/skills/agent-ready-setup), la skill de golfo-agent-ready que deja un repositorio listo para Claude Code y Codex.

El motor (scripts, hooks, settings, profiles de CI) vive en golfo-agent-ready. Acá está lo que proyecta:

- las rules y skills comunes;
- el template de `AGENTS.md`;
- los stacks (`node`, `react`, `nextjs`, `nextjs-app-router`, `java`, `go`, `android`);
- las capabilities (`software-development`, `business-flows`, `browser`, `learning`).

## Usarlo

Es la fuente de contenido por defecto de agent-ready-setup (`sources.golfo`, motor 0.90.0 o más nuevo): un repositorio que
no declara nada lo usa siguiendo `main`. Para fijarlo a una versión, en `.agents/agent-ready.json`:

```json
{
  "profiles": ["node"],
  "sources": {
    "golfo": { "ref": "v1.0.0", "updates": "pinned" }
  }
}
```

- `ref` puede ser un tag (recomendado para fijarlo), `main` o un commit completo.
- Con `"updates": "pinned"`, el repositorio queda en la revisión de su lock hasta `agent-ready update golfo`, y
  `agent-ready update golfo --to <tag>` adopta exactamente esa versión.
- Otro pack de contenido (un fork, un mirror) se declara con `"source": "git+https://..."` en el mismo objeto.

## Estructura

| Ruta | Qué tiene |
| --- | --- |
| `agent-ready-pack.json` | Catálogo: `version`, `minEngine`, `changes`, `baseAssets` y `profiles` |
| `base/` | Lo que recibe todo repositorio: rules, skills, bloques y `agents-template.md` |
| `stacks/<nombre>/` | Rules, skills, agents, commands y la sección de `AGENTS.md` de cada stack |
| `profiles/<nombre>/` | Capabilities, con `agents-skeleton.md` en `software-development` |
| `scripts/`, `tests/` | Chequeos del pack y su release |

## Versiones

Cada cambio al contenido sube `version` en `agent-ready-pack.json` y suma su entrada en `changes`. Al mergear a `main` se publica el tag `v<version>` con un release. Un tag publicado no se mueve.

## Contribuir

Las reglas para cambiar el pack (skills, rules, evals, versionado y chequeos) están en [AGENTS.md](AGENTS.md).
