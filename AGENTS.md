## What This Repository Is

The official content pack of [agent-ready-setup](https://github.com/guidomodarelli/golfo-marketplace/tree/main/plugins/golfo-kit/skills/agent-ready-setup), the skill of the golfo-kit plugin that sets up repositories for Claude Code and Codex. The engine (scripts, hooks, settings, CI profiles, provider capabilities) lives in golfo-kit; this repository holds the content it projects:

- `agent-ready-pack.json` — the catalog: `version`, `minEngine`, `changes`, `baseAssets` and the `profiles`.
- `base/` — what every repository gets: common rules, skills and blocks, and `agents-template.md`, the template of `AGENTS.md`.
- `stacks/<name>/` — each primary stack (`node`, `react`, `nextjs`, …): rules, skills, agents, commands, the stack section of `AGENTS.md` (`blocks/AGENTS.md`) and nested targets (`nested/`).
- `profiles/<name>/` — capabilities such as `software-development` (with `agents-skeleton.md`) and `business-flows`.
- `scripts/` — the checks of the pack (`check_pack.py`) and its release (`release.py`); `tests/` tests them.

This pack is the default content source of agent-ready-setup (`sources.golfo` in a repository's `.agents/agent-ready.json`, golfo-kit 0.90.0 or newer). The format is the one of `references/profiles-and-lockfile.md` of agent-ready-setup, section «El contenido».

## Mandatory Rules

1. **Use `/skill-creator`** to create or change a skill of the pack (its `SKILL.md`, references, scripts or evals under `base/skills/`, `stacks/*/skills/` or `profiles/*/skills/`).
2. **Run `/skill-optimizer` with `mode=audit`** on every skill you created or changed before reporting the work as done, and include its status. Escalate to `quick` or `full` only if the audit finds a measurable problem and the user agrees.
3. **Every `SKILL.md` follows the [Agent Skills specification](https://agentskills.io/specification)**: `name` in kebab-case, at most 64 characters and equal to its directory; `description` between 1 and 1024 characters, quoted when it contains `: `. `scripts/check_pack.py` enforces it.
4. **A new or changed skill comes with its evals** in `evals/eval-config.json`, run with `run-evals` of golfo-marketplace's `skill-eval-runner` (`run-evals <path-to-skill>`). `scripts/check_pack.py` lists the skills that still have none (they came from golfo-kit that way); one gets its evals the next time it changes.
5. **Rules are not skills.** A rule (`rules/*.md`) covers one concern and needs no `/skill-creator`. Every top-level bullet of a rule file is an atomic rule with its `<!-- rule id=<file>/<slug> -->` marker ([atomic-rules.md](https://github.com/guidomodarelli/golfo-marketplace/blob/main/plugins/golfo-kit/skills/agent-ready-setup/references/atomic-rules.md) of agent-ready-setup); `scripts/check_pack.py` fails on any error of `agent-ready rules lint`. The evals of the rules of a stack, a profile or `base/` live next to them, in `<dir>/evals/eval-config.json`, and run with `run-evals <dir>` (golfo-marketplace's `skill-eval-runner`, since guidomodarelli/golfo-marketplace#172, tells the agent to apply the rules of `<dir>/rules/`). A new or changed rule comes with a case there that fails without the rules (`run-evals --baseline`). A case that passes without the rules because the model already does it by default is a control case: mark it `"control": "<reason>"` (guidomodarelli/golfo-marketplace#179), so it guards that the rule does not contradict that default without counting as a case that fails to discriminate. It references another rule by its file name (`react-security.md#input-validation`), never by its path in this repository: projected, the rules of the root sit side by side in `.agents/rules/`. A new rule of a stack carries the stack prefix (`node-security.md`). The rules that came from golfo-kit without one keep their names, because other rules, the stack sections of `AGENTS.md` and the skills of golfo-kit reference them; the engine stops before writing if two profiles ever publish the same rule.
6. **Version every change to the content.** A pull request that changes `base/`, `stacks/`, `profiles/` or the catalog raises `version` (semver) in `agent-ready-pack.json` and adds its entry to `changes`, newest first, with `"breaking": true` when a consumer has to act (a profile removed or renamed, a rule that now asks for the opposite). Raise `minEngine` when the content uses something only a newer golfo-kit understands. The CI fails otherwise. A change limited to `evals/` directories needs no version: the engine never projects evals.
7. **Releases are tags.** Once the checks of a commit of `main` pass, the `release` job of `.github/workflows/check.yml` publishes `v<version>` as a tag and a GitHub release with the `changes` summary. A published tag never moves: consumers pin it.
8. **Nothing of the engine lives here.** Hooks, settings, CI profiles (`kind: ci`), configuration schemas and provider capabilities belong to golfo-kit; the engine rejects a pack that declares them.

## Checking a Change

```bash
# Tests of the checks
python3 -m unittest discover -s tests

# Catalog, skills and version against main, a projection of every profile and the lint of the atomic rules, with the engine
python3 scripts/check_pack.py --base origin/main \
  --engine ../golfo-marketplace/plugins/golfo-kit/skills/agent-ready-setup
```

The projection applies each profile in an empty repository of its own that takes the committed content of `HEAD` through `sources.golfo`, with a fake HOME and fake provider CLIs: it never starts a real agent. Commit before running it; uncommitted changes are not checked.

## Conventions

- Branches: `feature/<topic>`. Commits: `feat(content): …`, `fix(content): …`, `ci: …`.
- Pull requests describe the change for the repositories that consume the pack: what an agent will do differently.
- Single source of truth: a procedure or a convention lives in one file; the others reference it.
