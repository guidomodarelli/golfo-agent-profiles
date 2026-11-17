# Coding Style Rules — Go

<!-- rule id=go-coding-style/format-changed-file-gofmt -->
- Format every changed file with `gofmt` (or `goimports`) and keep `go vet` clean.
  - The project's linter configuration (for example `golangci-lint`) decides the remaining style.

<!-- rule id=go-coding-style/return-errors-last-value -->
- Return errors as the last value and handle them where they occur.
  - Wrap with context using `fmt.Errorf("operation: %w", err)` and compare with `errors.Is` or `errors.As`, never by message text.

<!-- rule id=go-coding-style/panic-expected-failures-reserve -->
- Do not `panic` for expected failures.
  - Reserve it for programmer errors during initialization.

<!-- rule id=go-coding-style/pass-context-context-first -->
- Pass `context.Context` as the first parameter of every function that performs I/O or can block, and propagate it instead of creating `context.Background()` mid-call.

<!-- rule id=go-coding-style/keep-packages-small-named -->
- Keep packages small and named by responsibility (`billing`, `httpapi`), never `util`, `common`, or `helpers`.
  - Accept interfaces and return concrete types.
  - Declare an interface in the package that consumes it.

<!-- rule id=go-coding-style/add-generic-abstractions-single -->
- Do not add generic abstractions with a single implementation.
  - See `Architecture and dependencies` in `patterns-we-do-not-use.md`.

<!-- rule id=go-coding-style/goroutine-has-owner-stop -->
- Every goroutine has an owner that can stop it (context cancellation or a closed channel) and waits for it to finish (`sync.WaitGroup` or `errgroup`).

<!-- rule id=go-coding-style/export-other-packages-document -->
- Export only what other packages use, and document every exported identifier with a comment that starts with its name.
