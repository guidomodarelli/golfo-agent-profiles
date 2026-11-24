---
trigger: always_on
---

# Patterns We Do Not Use

Each entry names a pattern to avoid, what to do instead, and why. A ban without an alternative leaves a gap that gets filled with the most familiar default, so apply the alternative, not only the ban. When an entry links another rule, that rule owns the procedure. Rules that link back here only point to the banned pattern; this file owns the entry: its alternative, reason, and exceptions.

## Architecture and dependencies

<!-- rule id=patterns-we-do-not-use/database-access-route-handlers -->
- **Database access from route handlers.** Route all persistence through the project's data access layer (repository, adapter, or service).
  - In Next.js projects, follow `hexagonal-architecture.md`.
  - Why: handlers that query directly spread schema knowledge and cannot be tested or changed in one place.
  - If the project has no such layer, follow the existing pattern instead of inventing one.

<!-- rule id=patterns-we-do-not-use/new-dependencies-platform-already -->
- **New dependencies for what the platform already covers.** Reuse the standard library, the framework, or a declared package first, as `established-libraries.md` defines.
  - Why: every dependency adds upgrades, supply chain risk, and a second way to do the same thing.

<!-- rule id=patterns-we-do-not-use/generic-abstractions-single-implementation -->
- **Generic abstractions with a single implementation.** Write the concrete code, and duplicate a few lines until a second real case shows what varies.
  - Why: an abstraction guessed from one case encodes the wrong axis of change.
  - Ports and adapters that `hexagonal-architecture.md` requires, and consumer-side interfaces a stack's `<stack>-coding-style.md` asks for, are not speculative.

<!-- rule id=patterns-we-do-not-use/configuration-options-just-case -->
- **Configuration options "just in case".** Add an option only with a current caller and a documented default.
  - Otherwise follow `speculative-complexity-approval.md`.
  - Why: unused options multiply the states to test and are rarely removed.

<!-- rule id=patterns-we-do-not-use/second-implementation-left-next -->
- **A second implementation left next to the old one.** Migrate every caller and delete the replaced path in the same change.
  - Why: two live paths drift, and nobody knows which one is the truth.
  - Exception: a gradual rollout behind an agreed feature flag, with the removal recorded as pending.

<!-- rule id=patterns-we-do-not-use/backward-compatibility-internal-apis -->
- **Backward compatibility for internal APIs nobody needs.** Update every caller in the same change instead of keeping shims, aliases, or optional legacy parameters.
  - Why: compatibility layers without consumers are dead code that still has to be maintained.
  - Exception: public or versioned APIs, external consumers, and persisted data formats.

## Errors and responses

<!-- rule id=patterns-we-do-not-use/fallbacks-hide-invalid-state -->
- **Fallbacks that hide invalid state.** Fail explicitly and keep the original error as the cause.
  - Why: a silent default turns a bug into wrong data that surfaces far from its origin.
  - Deliberate business fallbacks (see `root-cause-bug-fixes.md`) and adapter-approved defaults (see `react-security.md` in React projects) stay.

<!-- rule id=patterns-we-do-not-use/catching-exceptions-without-purpose -->
- **Catching exceptions without a purpose.** Catch only to recover, add useful context, or translate the error at a system boundary, as `Catch blocks` in `error-handling.md` defines.
  - Why: a catch that does none of these hides failures and loses the stack.

<!-- rule id=patterns-we-do-not-use/200-responses-carry-error -->
- **`200` responses that carry an error object.** Use the project's error types and the matching HTTP status (in React projects, see `Error Handling` in `react-security.md`).
  - Why: clients, caches, retries, and monitoring read the status, not the body.
  - Exception: protocols whose contract defines it, such as GraphQL's `errors` array or batch responses with partial results.

## Data

<!-- rule id=patterns-we-do-not-use/editing-migrations-have-been -->
- **Editing migrations that may have been applied.** Once a migration is merged or has run on a shared environment, add a new migration instead (see `database.md`).
  - Why: environments that already ran the old version never see the edit and drift silently.
  - Exception: a migration from the current branch that never ran outside a disposable database.

<!-- rule id=patterns-we-do-not-use/floating-point-money-store -->
- **Floating point for money.** Store and compute amounts as integer minor units or the project's decimal type, and format only for display.
  - Why: binary floats cannot represent most decimal amounts, so totals and rounding drift.

<!-- rule id=patterns-we-do-not-use/local-timestamps-persist-instants -->
- **Local timestamps.** Persist instants in UTC and convert to a time zone only at presentation boundaries.
  - Why: local times are ambiguous across DST changes and between servers.
  - Exception: calendar values without a time (a birth date) and the user's time zone stored separately when the domain needs it.

<!-- rule id=patterns-we-do-not-use/mocking-own-database-layer -->
- **Mocking your own database layer in integration tests.** Run them against the project's test database.
  - Why: a mocked database cannot catch query, schema, or transaction bugs.
  - Exception: unit and component tests that inject doubles at the port, as `testing-scope.md` and the stack's `<stack>-testing.md` allow.

## Security and UI

<!-- rule id=patterns-we-do-not-use/authorization-logic-client-enforce -->
- **Authorization logic in the client.** Enforce every permission on the server.
  - Why: anything in the client can be bypassed.
  - The client may hide or disable UI for usability, but it is never the control.

<!-- rule id=patterns-we-do-not-use/useeffect-derive-state-react -->
- **`useEffect` to derive state (React projects).** Compute derived values during render, and use `useMemo` only when the computation is measurably expensive.
  - Why: an effect that mirrors state adds an extra render and a frame of stale UI.
  - Effects stay for synchronizing with external systems.
  - For the detailed patterns, use the `react-render-performance-patterns` skill when it is installed.

## Project-specific patterns

This rule is managed: a local edit blocks its updates and is reported as a conflict. Record patterns specific to this project, such as lessons from a rejected implementation, in a project rule of your own under `.agents/rules/`, with a file name no managed rule uses.
