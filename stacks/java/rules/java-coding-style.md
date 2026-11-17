# Coding Style Rules — Java

<!-- rule id=java-coding-style/follow-formatter-static-analysis -->
- Follow the formatter and static analysis the build already configures (for example Spotless, Checkstyle, or Error Prone).
  - Do not reformat unrelated code.

<!-- rule id=java-coding-style/prefer-constructor-injection-final -->
- Prefer constructor injection with `final` fields.
  - Do not use field injection (`@Autowired` on fields).

<!-- rule id=java-coding-style/immutable-value-types-record -->
- Use immutable value types (`record`, `final` fields, unmodifiable collections) for DTOs and domain values.

<!-- rule id=java-coding-style/return-optional-instead-null -->
- Return `Optional` instead of `null` from lookups.
  - Never use `Optional` for fields or parameters.

<!-- rule id=java-coding-style/throw-specific-exceptions-carry -->
- Throw specific exceptions that carry context and the original cause.
  - Do not catch `Exception` or `Throwable` except at the boundary that maps errors to a response.

<!-- rule id=java-coding-style/close-resources-try-resources -->
- Close resources with try-with-resources.

<!-- rule id=java-coding-style/keep-controllers-thin-validate -->
- Keep controllers thin: validate and map the request, delegate to a service, and map the result to the response DTO.
  - Never return JPA entities from an API.

<!-- rule id=java-coding-style/declare-transaction-boundaries-transactional -->
- Declare transaction boundaries (`@Transactional`) on service methods, not on controllers or repositories.
