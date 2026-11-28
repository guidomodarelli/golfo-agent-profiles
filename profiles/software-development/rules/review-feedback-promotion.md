---
trigger: always_on
---

# Review Feedback Promotion

A review finding fixed once can come back in the next change. Every new kind of error a review finds becomes an automated check, so the harness catches it without a reviewer the next time.

## Promote new kinds of errors

<!-- rule id=review-feedback-promotion/new-kind-gets-check -->
- When a review finds a kind of error that no automated check of the project covers yet, fix it and add, in the same change, an automated check that fails without the fix.
  - The review can come from a person, a review bot (Codex, Claude), the agent's own review, or a defect the user reports after the agent called the work done.
  - A kind of error is the general pattern, not the single line: «a handler that swallows a database error and answers 200», not «line 42 of `orders.ts`».
  - Except: a finding closed without changes (an unrealistic edge case, a pre-existing defect left out of scope, a non-blocking nit) gets no check.

<!-- rule id=review-feedback-promotion/cheapest-check-that-fails -->
- Choose the cheapest check that fails on the error, in this order: a lint rule, a regression test at the layer where the error shows (unit, integration or end-to-end), a pre-push or CI check.
  - An error that crosses components (an interface, state passed between layers, a resource lifetime, the real environment) needs an integration or end-to-end check: a unit test with mocks cannot see it.
  - When the error depends on the shape of the input and the project already uses a property-based testing library, a property over generated inputs covers the whole kind of error; check that the generated cases are not mostly trivial (empty or one-element inputs).
  - When you add or change a lint rule, follow `lint-gate.md`.
  - A test follows `testing-scope.md`: a check that only reads committed files to match their text runs as a lint rule or a pre-push or CI script, not as a test file, unless the project's `AGENTS.md` requires that test.

<!-- rule id=review-feedback-promotion/prove-check-fails -->
- Prove the check fails without the fix before relying on it: run it against the code before the fix, or against a deliberately broken copy, and confirm it reports.

<!-- rule id=review-feedback-promotion/existing-check-name-it -->
- When an existing check already covers the kind of error, do not add another: name that check when closing the finding.
  - If the existing check should have failed and did not, fix that check instead.

<!-- rule id=review-feedback-promotion/not-automatable-becomes-rule -->
- When a kind of error cannot be checked automatically (a judgment of design, naming or wording), record it as a project rule under `.agents/rules/` instead, and say why no check applies.

<!-- rule id=review-feedback-promotion/check-message-actionable -->
- Make the failure message of a new check say what is wrong and where (file and line), why it is a problem, and how to fix it (the module, API or pattern to use instead).
  - The agent reads that message and fixes the code from it, without a reviewer.

## Record promoted findings

<!-- rule id=review-feedback-promotion/record-in-versioned-registry -->
- Record each promoted kind of error in the project's versioned registry of promoted findings, in the same change as its check.
  - The registry is the file the project's `AGENTS.md` names for it, or `docs/review-findings.md` when it names none; create it with its header the first time.
  - Each entry is a row of a table with: the date (`YYYY-MM-DD`), the kind of error, where it was found (a link to the review comment, or `own review`), the check that covers it (its path and the command that runs it, or the project rule for one that cannot be automated) and the change that added it.
  - Never record secrets, personal data or raw payloads in the registry.

<!-- rule id=review-feedback-promotion/read-registry-before-review -->
- Before reviewing or closing a finding, read the registry: a kind of error already recorded means its check exists, so a finding of that kind that still got through is a gap in that check.

<!-- rule id=review-feedback-promotion/closing-names-check -->
- When closing a fixed review finding, say which automated check covers it, or why none applies.
  - In a reply to a review comment, that is one line, for example «Verificación: regression test `tests/orders-handler.test.ts`, fails without the fix» or «Verificación: no aplica: wording change without behavior to check».
