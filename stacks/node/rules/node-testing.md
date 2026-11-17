# Testing Rules — Node

<!-- rule id=node-testing/test-runner-project-already -->
- Use the test runner the project already configures (Jest, Vitest, or `node:test`).
  - Do not introduce a second one.

<!-- rule id=node-testing/test-http-routes-through -->
- Test HTTP routes through the real app (for example with Supertest) and assert status, headers, and body as the client sees them.

<!-- rule id=node-testing/replace-dependencies-boundaries-project -->
- Replace dependencies at the boundaries the project owns (repositories, outbound clients).
  - Do not mock Node built-ins or the framework.

<!-- rule id=node-testing/await-async-assertion-fail -->
- Await every async assertion and fail on unhandled rejections.
  - Instead of fixed `sleep` delays, use fake timers or wait for the observable condition.

<!-- rule id=node-testing/run-repository-sql-tests -->
- Run repository and SQL tests against a real database (a container or the project's test database).

<!-- rule id=node-testing/mock-own-database-layer -->
- Do not mock your own database layer in integration tests.
  - See `Data` in `patterns-we-do-not-use.md`.
