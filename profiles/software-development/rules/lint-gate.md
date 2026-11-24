---
trigger: always_on
---

# Lint Gate

A task that adds or modifies files is not complete until applicable project lint validation succeeds.

<!-- rule id=lint-gate/run-repository-s-configured -->
- Run the repository's configured lint command once at the end of the task, after all edits are done.
  - Do not run it after every individual file change.

<!-- rule id=lint-gate/task-complete-lint-command -->
- The task is complete only when the lint command exits with code 0.
  - Warnings do not block unless repository configuration says otherwise.
  - Errors do.

<!-- rule id=lint-gate/fix-lint-error-within -->
- Fix every lint error within the same task before closing it.
  - Do not leave lint errors for a follow-up.

<!-- rule id=lint-gate/silence-lint-inline-disable -->
- Do not silence lint with inline disable directives (`eslint-disable`, `oxlint-disable`, or equivalents).
  - Fix the reported code instead.

<!-- rule id=lint-gate/add-change-lint-rule -->
- When you add or change a lint rule or plugin, run the linter against a deliberately violating change and confirm it reports before relying on it: a plugin that fails to load produces no diagnostics.

<!-- rule id=lint-gate/project-has-configured-linter -->
- If the project has no configured linter, report `N/A` and do not add one only to satisfy this rule.
  - If the lint command cannot run (for example, missing dependencies or environment limitations), report the reason and pending validation.
