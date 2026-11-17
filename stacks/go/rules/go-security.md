# Security Rules — Go

<!-- rule id=go-security/hardcode-secrets-tokens-credentials -->
- Never hardcode secrets, tokens, or credentials.
  - Read them from environment variables or the project's secret manager, and never log them.

<!-- rule id=go-security/validate-untrusted-input-request -->
- Validate every untrusted input (request body, query, path parameters, headers) at the handler boundary before it reaches business logic, using an allowlist.

<!-- rule id=go-security/build-sql-placeholders-1 -->
- Build SQL only with placeholders (`$1`, `?`) through `database/sql` or the project's query builder.
  - Never concatenate or `fmt.Sprintf` user input into a query.

<!-- rule id=go-security/run-external-commands-exec -->
- Run external commands with `exec.CommandContext` and separate arguments.
  - Never pass user input to a shell (`sh -c`).

<!-- rule id=go-security/resolve-user-supplied-file -->
- Resolve user-supplied file paths with `filepath.Clean` and confirm they stay inside the allowed root before opening them.

<!-- rule id=go-security/give-outbound-http-client -->
- Give every outbound `http.Client` and every `http.Server` explicit timeouts.
  - Never rely on the zero-timeout defaults for network calls.

<!-- rule id=go-security/crypto-rand-tokens-identifiers -->
- Use `crypto/rand` for tokens and identifiers that must not be guessable.
  - Never `math/rand`.

<!-- rule id=go-security/return-safe-error-messages -->
- Return safe error messages to clients.
  - On the server, log the failure as `error-handling.md` › `Diagnosable failures` defines: the cause chain as error type names and closed codes plus opaque identifiers, never stacks, messages, SQL, or provider payloads.

<!-- rule id=go-security/run-govulncheck-dependencies-change -->
- Run `govulncheck ./...` when dependencies change and resolve the vulnerabilities reported in called code.
