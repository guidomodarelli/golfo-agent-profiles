# Security Rules — Node

<!-- rule id=node-security/hardcode-secrets-tokens-credentials -->
- Never hardcode secrets, tokens, or credentials.
  - Read them from environment variables or the project's secret manager, and never log them.

<!-- rule id=node-security/build-sql-parameterized-queries -->
- Build SQL only with parameterized queries through the project's driver or query builder.
  - Never interpolate user input into a query.

<!-- rule id=node-security/run-external-commands-execfile -->
- Run external commands with `execFile` or `spawn` and an argument array.
  - Never pass user input to `exec` or a shell.

<!-- rule id=node-security/pass-untrusted-input-eval -->
- Never pass untrusted input to `eval`, `new Function`, `vm`, or a dynamic `require`/`import`.

<!-- rule id=node-security/merge-untrusted-objects-existing -->
- Do not merge untrusted objects into existing ones (`Object.assign`, deep merge) without an allowlist of keys.
  - Reject `__proto__`, `constructor`, and `prototype`.

<!-- rule id=node-security/return-safe-error-messages -->
- Return safe error messages to clients.
  - On the server, log the failure as `error-handling.md` › `Diagnosable failures` defines: the cause chain as error type names and closed codes plus opaque identifiers, never stacks, messages, SQL, or provider payloads.

<!-- rule id=node-security/run-npm-audit-package -->
- Run `npm audit` (or the package manager's equivalent) when dependencies change and resolve reported vulnerabilities.

## Payload Validation Boundaries

Keep three payloads apart: client input received by the service, the public DTO the service returns to its consumers, and responses from backend/upstream providers.

### Client input

<!-- rule id=node-security/validate-req-body-req -->
- Validate `req.body`, `req.query`, `req.params`, and every client-controlled header the route reads at the service's entry boundary: they are untrusted input, and the boundary is the only place to reject them before business logic runs.

<!-- rule id=node-security/validation-library-repository-already -->
- Use the validation library the repository already adopted (for example, zod).
  - Add a new one only when none exists or it cannot express the requirement.

<!-- rule id=node-security/validate-route-once-handlers -->
- Validate each route once.
  - Handlers consume the validated values and keep only business rules that the schema cannot express.

<!-- rule id=node-security/allowlist-define-permitted-reject -->
- Use an allowlist: define what is permitted and reject everything else, without echoing input values in the error.

### Public DTO

<!-- rule id=node-security/validate-dto-service-returns -->
- Validate the DTO the service returns to its consumers before handing it over: it is the service's own contract, and validating it keeps internal fields and inconsistent shapes from leaking.

<!-- rule id=node-security/allowlist-public-fields-types -->
- Allowlist its public fields, types, states, and discriminators.
  - Reject an unusable DTO safely, without exposing internal diagnostics.

### Upstream responses

<!-- rule id=node-security/revalidate-backend-upstream-responses -->
- Never revalidate backend/upstream responses as if they were client input: the provider owns that contract, and revalidating it couples the service to fields it does not consume and breaks on compatible upstream changes.

<!-- rule id=node-security/add-schemas-validation-middleware -->
- Do not add schemas, validation middleware, field-by-field checks, type guards, or `normalize*Response`/`parse*Response` helpers for provider success or error payloads.

<!-- rule id=node-security/consume-response-according-adapter -->
- Consume the response according to the adapter contract.
  - Narrow structurally only when control flow or safe access requires it: prefer the HTTP status, distinguish `null`, `array`, and `object` when that changes the flow, and read minimum discriminators such as `PROCESSING` or `FINISHED`.
  - That narrowing never becomes a full field allowlist.

<!-- rule id=node-security/response-cannot-consumed-map -->
- If the response cannot be consumed, map a controlled failure in the adapter or service.
  - Never forward the raw payload.

<!-- rule id=node-security/request-upstream-response-validation -->
- Never request upstream response validation in reviews, fixes, verifications, or closeouts.

### Decision order

<!-- rule id=node-security/check-http-status-available -->
1. Check the HTTP status and the available transport metadata.

<!-- rule id=node-security/narrow-structurally-control-flow -->
2. Narrow structurally only if control flow requires it.

<!-- rule id=node-security/client-input-run-schema -->
3. For client input, run schema validation at the boundary, before the handler.

<!-- rule id=node-security/public-dto-run-guard -->
4. For the public DTO, run its guard or contract validation before handing it to the consumer.

<!-- rule id=node-security/turn-observation-upstream-response -->
5. Never turn an observation of an upstream response into full revalidation of that response.

### Required tests

<!-- rule id=node-security/invalid-client-input-rejected -->
- Invalid client input is rejected at the boundary.

<!-- rule id=node-security/valid-public-dto-reaches -->
- A valid public DTO reaches the consumer, and an unusable DTO is rejected safely.

<!-- rule id=node-security/upstream-responses-consumed-without -->
- Upstream responses are consumed without schema revalidation.

<!-- rule id=node-security/processing-finished-array-object -->
- `PROCESSING`/`FINISHED`, `array`/`object`, or `null` are distinguished only where they change control flow.

<!-- rule id=node-security/handlers-validate-again-boundary -->
- Handlers do not validate again what the boundary already validated.

<!-- rule id=node-security/raw-upstream-payloads-reach -->
- Raw upstream payloads never reach responses, logs, or public errors.

<!-- rule id=node-security/tests-exercise-real-validator -->
- Tests exercise the real validator and its observable contract.
  - Do not mock the validator.
