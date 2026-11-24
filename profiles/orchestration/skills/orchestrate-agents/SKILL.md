---
name: orchestrate-agents
description: >-
  Procedimiento genérico para repartir una tarea entre los subagentes de un roster
  y consolidar sus resultados en un solo informe: partir la tarea, despachar a cada
  subagente lo suyo, juntar las respuestas, resolver contradicciones y decir qué
  quedó sin cubrir. Usar desde un command o una skill que aporta el roster (una
  tabla de archivos `.agents/agents/<nombre>.md`), o cuando pidan "revisalo con
  todos los agentes", "que lo vean el contador y el auditor", "repartilo entre los
  subagentes" o "consolidá lo que dijeron los agentes". Corre en la sesión
  principal. No usar para una tarea que una sola skill resuelve sin subagentes.
license: MIT
metadata:
  version: "1.0.0"
  tags: "orchestration, subagents, roster, multi-provider"
---

# Orchestrate agents

Single source for dispatching a task to a roster of subagents and consolidating what they return. The
profile that needs it (a stack, an office, a team) provides only its **roster**: a table with the file
`.agents/agents/<name>.md` of each subagent and when it applies. This skill provides the procedure.

Run it in the main session. In Claude Code, Codex and Antigravity a subagent does not start other subagents
by default, so the orchestrator is the session that talks with the user, never one of the subagents.

## 1. Read the roster

Take the roster from the command or skill that called this one. Each row names a subagent file and, when
it is not "always", the condition that activates it.

- Read each subagent file before dispatching: its `description` and body say what it covers and what it
  needs as input.
- A row whose file does not exist is not dispatched: report it under **Not covered** with its path. Never
  improvise that subagent's role in the main session, because the user would believe it was reviewed
  independently.
- **Without a roster** (nobody provided one and the request just says "use the agents"), list
  `.agents/agents/` and ask the user, in one question, which of them to use for this task. Do not dispatch
  to every subagent by default: each one costs a full context and its own tokens.

## 2. Split the task

Give each subagent only what its role needs: the files, the diff, the document or the question, plus the
goal of the whole task in one line. A subagent starts with an empty context, so it never sees this
conversation: everything it needs goes in its brief.

- Dispatch the independent subagents in parallel; keep in order only the ones whose input is another's
  output.
- Respect each activation condition; a skipped subagent goes under **Not covered** with the reason.

## 3. Consolidate

Wait for every dispatched subagent before reporting. Then:

- **Merge duplicates:** the same finding from two subagents is one item that names both.
- **Resolve contradictions:** when two subagents disagree, check the evidence each one gives against the
  source (the file, the figure, the rule). Keep the one the evidence supports and say why in one line. If
  the evidence cannot decide it, keep both under **To decide** with the question the user has to answer.
- **Keep what each one could not do:** a subagent that could not run a tool or read a file says so in its
  answer; carry it to **Not covered**.

## 4. Report

```
## <Task> — consolidated

### 🔴 Blocking
- [agent] [where] Finding — Fix: ...

### 🟡 Recommended
- [agent] [where] Suggestion.

### ⚖️ To decide
- [agent A] vs [agent B]: what each says — Question: ...

### Not covered
- [agent or file]: why (missing file, activation condition, tool it could not run).
```

Leave out an empty section, except **Not covered**: say "nothing" there, so the reader knows every row of
the roster ran. A roster can add its own sections or severity rules (for example, a code review marks lint
errors as blocking); they extend this report, never replace it.
