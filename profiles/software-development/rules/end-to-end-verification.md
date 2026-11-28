---
trigger: always_on
---

# End-to-End Verification

Unit tests isolate each part, so they cannot see defects in the boundaries between parts: every part can pass its tests while the system fails. A change that crosses components is verified through the real flow.

## Levels of verification

<!-- rule id=end-to-end-verification/levels-by-change -->
- Verify each change at the levels its reach requires: unit tests for logic inside one module, integration tests for a module with its real dependencies (database, framework, another module), and an end-to-end run of the affected flow when the change crosses components.
  - A change crosses components when it touches the contract or the data passed between two of them: a client and its server, a route and its service, a process and its worker, a migration and the code that reads the table, a producer and its consumer.
  - Choose the smallest command of each level, as `verify-changes.md` defines.

<!-- rule id=end-to-end-verification/skipped-level-not-done -->
- A change that skipped a level it requires is not done.
  - Report the skipped level, why it could not run, and what remains unverified, instead of reporting the change as done.

<!-- rule id=end-to-end-verification/cross-component-defects -->
- When a change crosses components, check through the end-to-end run the defects that unit tests miss.
  - Mismatched interfaces: paths, formats or names that each side reads differently.
  - State or progress that does not propagate between layers.
  - Resources that are not released: handles, connections, sockets.
  - Behavior that changes in the real environment: permissions, packaging, configuration.
  - Errors of one layer that never reach the user.

<!-- rule id=end-to-end-verification/missing-e2e-harness -->
- When the project has no end-to-end harness for a flow a change crosses, run the flow by hand in the real application, and report that the flow has no automated end-to-end coverage.
  - Do not add an end-to-end framework only to satisfy this rule: propose it to the user.

## Executable constraints

<!-- rule id=end-to-end-verification/constraints-executable -->
- Turn each architecture constraint the project states (which layer may import which, where input is parsed, which module owns an external call) into an automated check: a lint rule, a dependency rule, or a pre-push or CI script.
  - A constraint that lives only in a document gets broken: agents copy the patterns they find in the code, the bad ones too.
  - Follow `review-feedback-promotion.md` for the check's failure message and for checks born from a review finding.
