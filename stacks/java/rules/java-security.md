# Security Rules — Java

<!-- rule id=java-security/hardcode-secrets-tokens-credentials -->
- Never hardcode secrets, tokens, or credentials.
  - Read them from environment variables or the project's secret manager, and never log them.

<!-- rule id=java-security/validate-request-dtos-controller -->
- Validate request DTOs at the controller boundary with Bean Validation (`@Valid` plus constraint annotations) and reject unknown or invalid values with an allowlist.

<!-- rule id=java-security/parameterized-queries-preparedstatement-jpa -->
- Use parameterized queries (`PreparedStatement`, JPA parameters, Spring Data methods).
  - Never concatenate user input into SQL or JPQL.

<!-- rule id=java-security/deserialize-untrusted-data-java -->
- Do not deserialize untrusted data with Java native serialization (`ObjectInputStream`).
  - Configure JSON mappers without default typing for untrusted input.

<!-- rule id=java-security/keep-authorization-checks-security -->
- Keep authorization checks in the security configuration or the service layer (for example `@PreAuthorize`), never only in the client.

<!-- rule id=java-security/return-safe-error-messages -->
- Return safe error messages to clients.
  - On the server, log the failure as `error-handling.md` › `Diagnosable failures` defines: the cause chain as error type names and closed codes plus opaque identifiers, never stacks, messages, SQL, or provider payloads.

<!-- rule id=java-security/scan-dependencies-owasp-dependency -->
- Scan dependencies (OWASP Dependency-Check or the project's tool) when they change and resolve reported vulnerabilities.
