# Testing Rules — Go

<!-- rule id=go-testing/standard-testing-package-table -->
- Use the standard `testing` package with table-driven tests and `t.Run` subtests named after the scenario.

<!-- rule id=go-testing/run-go-test-race -->
- Run `go test -race ./...` for changes that touch goroutines, channels, or shared state.

<!-- rule id=go-testing/mark-helpers-t-helper -->
- Mark helpers with `t.Helper()`, register cleanup with `t.Cleanup`, and use `t.TempDir()` for files instead of fixed paths.

<!-- rule id=go-testing/replace-dependencies-through-interfaces -->
- Replace dependencies through the interfaces the consuming package declares (hand-written fakes are preferred).
  - Do not mock the standard library.

<!-- rule id=go-testing/test-http-handlers-net -->
- Test HTTP handlers with `net/http/httptest` and assert status, headers, and body as the client sees them.

<!-- rule id=go-testing/keep-tests-need-external -->
- Keep tests that need external services (database, network) behind a build tag or `testing.Short()` so the default unit run stays hermetic.
