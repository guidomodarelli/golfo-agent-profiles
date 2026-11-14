# golfo-agent-profiles

Pack oficial de contenido de [agent-ready-setup](https://github.com/guidomodarelli/golfo-marketplace/tree/main/plugins/golfo-kit/skills/agent-ready-setup), la skill de golfo-kit que deja un repositorio listo para Claude Code y Codex.

El motor (scripts, hooks, settings, profiles de CI) vive en golfo-kit. Acá está lo que proyecta:

- las rules y skills comunes;
- el template de `AGENTS.md`;
- los stacks (`node`, `react`, `nextjs`, `nextjs-app-router`, `java`, `go`, `android`);
- las capabilities (`software-development`, `business-flows`, `browser`).

## Usarlo

En `.agents/agent-ready.json` del repositorio:

```json
{
  "profiles": ["node"],
  "sources": {
    "golfoKit": { "source": "git+https://github.com/guidomodarelli/golfo-agent-profiles", "ref": "v1.0.0" }
  }
}
```

- `ref` puede ser un tag (recomendado), `main` o un commit completo.
- Con `"updates": "pinned"`, el repositorio queda en la revisión de su lock hasta `agent-ready update golfo-kit`.
- Necesita golfo-kit 0.88.0 o más nuevo.

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
