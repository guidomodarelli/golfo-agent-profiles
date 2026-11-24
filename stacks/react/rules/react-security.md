---
trigger: always_on
---

# Security Rules — React + TypeScript

Baseline security rules for SSR React applications. These rules are always active and condition all code generation. The `react-security-scanner` agent uses this file as its baseline checklist and as supplementary context for the findings of any configured security tool.

---

## Secrets & PII

<!-- rule id=react-security/hardcode-secrets-tokens-api -->
- Never hardcode secrets, tokens, or API keys — read them at runtime from the project's secrets manager.

<!-- rule id=react-security/log-pii-emails-phone -->
- Never log PII (emails, phone numbers, names, addresses, document numbers), raw request or response payloads, or credentials (secrets, tokens, cookies, authorization headers).
  - Use the project's logger.

<!-- rule id=react-security/opaque-stable-identifiers-allowed -->
- Opaque, stable identifiers are allowed in logs and are expected for debugging: `userId`, `requestId`, `traceId`, and resource IDs.
  - They must be internal identifiers, never a PII value used as an identifier (for example, an email as a user key).

<!-- rule id=react-security/receive-pii-tokens-query -->
- Never receive PII or tokens via query parameters — use request body.

<!-- rule id=react-security/expose-sensitive-data-react -->
- Never expose sensitive data in React state or Context, nor in a client store if the project uses one — keep it server-side only.

## Input Validation

<!-- rule id=react-security/middleend-endpoints-validate-untrusted -->
- Middleend endpoints must validate all untrusted client-controlled request inputs (body, query params, path params, headers) at the controller/handler boundary using the project's input validation library (for example, zod).

<!-- rule id=react-security/validate-route-once-boundary -->
- Validate each route once at that boundary.
  - Handlers consume the already validated values and keep only business rules that the schema cannot express.

<!-- rule id=react-security/validate-public-dto-middleend -->
- Validate the public DTO that the middleend returns to its client or consumer before handing it over: that DTO is the middleend's own contract, and validating it keeps internal fields and inconsistent shapes from leaking.
  - Reject an unusable DTO safely, without exposing internal diagnostics.

<!-- rule id=react-security/revalidate-payloads-received-backend -->
- Never revalidate payloads received from backend/upstream services.
  - They are response data, not client input.
  - Consume them according to the adapter contract instead of adding a second validation step.

<!-- rule id=react-security/validate-complete-format-contract -->
- Never validate the complete format or contract of a backend/upstream success payload or error payload at runtime.
  - Do not add a schema, allowlist, field-by-field check, type guard, or error-shape parser for the provider response.

<!-- rule id=react-security/prefer-safe-fallback-structural -->
- Prefer a safe fallback before structural narrowing when absence, `null`, `undefined`, or an intentionally empty value can use an adapter-approved default.
  - Use `??` for nullish fallback and `||` only when every falsy value is intentionally equivalent to absence.
  - Never use a fallback that fabricates authorization, eligibility, ownership, success, or provider facts.

<!-- rule id=react-security/structural-narrowing-changes-control -->
- Use structural narrowing only when it changes control flow or enables safe access and no safe fallback exists.
  - Valid examples are HTTP status or transport metadata, `null` versus `array` versus `object`, or a minimum discriminator such as `PROCESSING` or `FINISHED`.
  - This narrowing is not upstream contract verification and must not become a complete field allowlist, type guard, or error-shape parser.

<!-- rule id=react-security/add-normalizeresponse-parseresponse-helper -->
- Never add a `normalize*Response`/`parse*Response` helper, response-shape guard, field-by-field response validator, or client-error throw solely because an upstream or backend response differs from an expected shape.
  - Apply approved defaults first.
  - Narrow only to choose a flow or avoid unsafe access.

<!-- rule id=react-security/upstream-response-cannot-consumed -->
- If an upstream response cannot be consumed after safe fallback and the minimum flow discriminator is unavailable, continue with the adapter's safe empty/default projection when the contract permits it.
  - Otherwise map a controlled integration failure without forwarding the raw payload or introducing full contract validation.

<!-- rule id=react-security/whenever-code-needs-validate -->
- Whenever code needs to validate a variable, function argument, method argument, or intermediate value that is not a backend/upstream response payload, prefer the project's input validation library over native validation.

<!-- rule id=react-security/input-validation-library-cannot -->
- If the input validation library cannot express the complete requirement, keep it as the primary validation and add only the narrowly scoped native checks that are still necessary, such as `Number.isSafeInteger`.

<!-- rule id=react-security/allowlist-strategy-client-controlled -->
- Use allowlist strategy for client-controlled inputs and public middleend DTOs — define what is permitted, reject everything else.

<!-- rule id=react-security/trust-user-provided-identifiers -->
- Never trust user-provided identifiers directly — retrieve user identity from session or JWT claims.

### Validation decision order

<!-- rule id=react-security/check-http-status-available -->
1. Check the HTTP status and the available transport metadata.

<!-- rule id=react-security/apply-adapter-approved-safe -->
2. Apply an adapter-approved safe fallback, then structural narrowing only if control flow still requires it.

<!-- rule id=react-security/client-input-run-schema -->
3. For client input, run schema validation at the middleend boundary, before the handler.

<!-- rule id=react-security/public-middleend-dto-run -->
4. For the public middleend DTO, run its guard or contract validation before handing it to the client or consumer.

<!-- rule id=react-security/turn-observation-upstream-response -->
5. Never turn an observation of an upstream response into full revalidation of that response.

Never request upstream response validation in reviews, fixes, verifications, or closeouts.

### Validation tests

<!-- rule id=react-security/invalid-client-input-rejected -->
- Invalid client input is rejected at the middleend boundary.

<!-- rule id=react-security/valid-public-dto-reaches -->
- A valid public DTO reaches the consumer, and an unusable DTO is rejected safely.

<!-- rule id=react-security/upstream-responses-consumed-without -->
- Upstream responses are consumed without schema revalidation.

<!-- rule id=react-security/processing-finished-array-object -->
- `PROCESSING`/`FINISHED`, `array`/`object`, or `null` are distinguished only where they change control flow.

<!-- rule id=react-security/handlers-validate-again-boundary -->
- Handlers do not validate again what the boundary already validated.

<!-- rule id=react-security/raw-upstream-payloads-reach -->
- Raw upstream payloads never reach responses, logs, or public errors.

<!-- rule id=react-security/tests-exercise-real-validator -->
- Tests exercise the real validator and its observable contract.
  - Do not mock the validator.

## XSS Prevention

<!-- rule id=react-security/dangerouslysetinnerhtml-untrusted-content-dompurify -->
- Never use `dangerouslySetInnerHTML` with untrusted content — use `DOMPurify` if HTML rendering is required.

<!-- rule id=react-security/inject-raw-json-js -->
- Never inject raw JSON or JS objects into HTML responses — use a safe serializer that escapes HTML-sensitive characters (for example, `serialize-javascript`).

<!-- rule id=react-security/weaken-bypass-content-security -->
- Never weaken or bypass Content Security Policy (CSP).

## HTTP & Outbound Calls

<!-- rule id=react-security/project-s-http-client -->
- Use the project's HTTP client for all external HTTP calls.

<!-- rule id=react-security/pass-user-controlled-input -->
- Never pass user-controlled input directly to `fetch`, `axios`, or `http.request` — validate destinations against a static allowlist.

<!-- rule id=react-security/get-state-modifying-operations -->
- Never use GET for state-modifying operations.

<!-- rule id=react-security/configure-cors-without-formal -->
- Never configure CORS without formal security review — never use wildcards (`*`).

## Secure Coding

<!-- rule id=react-security/math-random-crypto-randombytes -->
- Never use `Math.random()` — use `crypto.randomBytes()` or `crypto.randomInt()` from `node:crypto`.

<!-- rule id=react-security/sequential-predictable-identifiers-auto -->
- Never use sequential or predictable identifiers (auto-increment, UUID v1/v6/v7, timestamp-based) — use `crypto.randomUUID()` from `node:crypto` (UUID v4).

<!-- rule id=react-security/string-concatenation-sql-queries -->
- Never use string concatenation for SQL queries — use parameterized queries or ORM.

<!-- rule id=react-security/eval-function-settimeout-setinterval -->
- Never use `eval()`, `Function()`, or `setTimeout`/`setInterval` with strings.

<!-- rule id=react-security/deprecated-crypto-md5-sha1 -->
- Never use deprecated crypto (MD5, SHA1, DES, RC4) — use AES-256, SHA-256, RSA-2048+.

<!-- rule id=react-security/regexes-exponential-complexity-user -->
- Never use regexes with exponential complexity on user input — validate for ReDoS resistance.

## Error Handling

Treat the middleend/BFF as an error-origin boundary: preserve statuses received from upstream, and translate only failures owned by the BFF into its public HTTP contract.

<!-- rule id=react-security/preserve-http-status-received -->
- Preserve the HTTP status received from upstream, including upstream 4xx and 5xx.
  - The BFF may sanitize or adapt the public error body, but must not replace an upstream status with a BFF-owned status merely because the payload is being translated.

<!-- rule id=react-security/failures-owned-bff-attributable -->
- For failures owned by the BFF and attributable to the request or domain state, return the corresponding 4xx.
  - `400` for malformed requests, `401` for missing or invalid authentication, `403` for insufficient permissions, `404` for missing resources, `409` for state conflicts, or `422` for semantically invalid or unprocessable input.

<!-- rule id=react-security/failures-owned-bff-genuinely -->
- For failures owned by the BFF that are genuinely unexpected or internal, return an appropriate 5xx.
  - Use `502`/`504` for integration failures such as an upstream transport failure, timeout, or response without a usable HTTP status.
  - Choose the status according to the failure cause.

<!-- rule id=react-security/generic-5xx-fallback-known -->
- Do not use a generic 5xx fallback for a known BFF client/domain error, and do not convert an upstream 4xx into a BFF 5xx.
  - Preserve a safe public message and log the diagnostic cause server-side without exposing internals.

<!-- rule id=react-security/classify-hydration-partial-attribute -->
- Do not classify hydration or partial-attribute failures by symptom alone.
  - First identify the origin: when client-controlled input or domain state caused incomplete attributes, map the cause to its applicable BFF-owned 4xx.
  - When upstream transport/status metadata or adapter classification identifies a dependency failure, preserve the upstream status or map a no-status integration failure to the appropriate 5xx.
  - Do not validate the full upstream success or error payload to make that classification.

<!-- rule id=react-security/adapter-cannot-consume-upstream -->
- If the adapter cannot consume an upstream response, map a controlled integration failure at that boundary without forwarding the raw payload or introducing full upstream contract validation.

<!-- rule id=react-security/keep-upstream-status-reporting -->
- Keep upstream status reporting truthful in every diagnostic artifact (error tracking details, structured logs, metrics): report only the real HTTP status returned by the upstream dependency, and report `unknown` when the dependency returned no status.
  - A BFF-synthesized `503`/`504` chosen as the public response status is never the upstream status and must not be labeled as one.
  - When the BFF owns a status mapping, keep it separate from the reported upstream status so diagnostics never invent upstream facts.

<!-- rule id=react-security/shared-helper-extracts-http -->
- When a shared helper extracts an HTTP status from a caught error to report it as the upstream status, never let it read that status from the BFF's own typed/domain error classes.
  - A malformed-payload error, a domain validation error, or a rule/eligibility classification carries a `status` the BFF assigned for its own public contract, not a fact the dependency reported.
  - Give any error that legitimately wraps a real dependency failure its own explicit `upstreamStatus` field, populated only from that failure, and have the shared helper trust that field (an `instanceof` check on the BFF's own error hierarchy, or equivalent) instead of falling back to `status`/`response.status` for those classes.
  - Reserve that fallback for raw, unclassified transport rejections.
  - Test both origins: a raw upstream failure and a BFF-owned typed-error failure must never produce the same reported upstream status.

<!-- rule id=react-security/expose-stack-traces-internal -->
- Never expose stack traces or internal error details to users — return generic messages.

<!-- rule id=react-security/log-sensitive-data-error -->
- Never log sensitive data in error handlers.
  - Log the error type, its stable code, and the opaque identifiers of the operation instead (see `error-handling.md`).

<!-- rule id=react-security/return-200-responses-carry -->
- Do not return `200` responses that carry an error object.
  - See `Errors and responses` in `patterns-we-do-not-use.md`.

## Authorization

<!-- rule id=react-security/project-s-approved-authentication -->
- Use the project's approved authentication and authorization libraries for all new auth/authz implementations.
  - Never hand-roll them.

<!-- rule id=react-security/validate-user-actions-follow -->
- Always validate that user actions follow valid business workflows server-side.

<!-- rule id=react-security/enforce-critical-business-logic -->
- Never enforce critical business logic validations from user-controlled input.

<!-- rule id=react-security/put-authorization-logic-client -->
- Do not put authorization logic in the client.
  - See `Security and UI` in `patterns-we-do-not-use.md`.
