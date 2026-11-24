---
trigger: always_on
---

# User-Facing Feedback Rules — SSR + React

These rules apply when a critical or async action modifies, loads, or requests data: submit, search, navigation, edit, retry, or mutation. For user-facing copy wording, see `User-facing copy` in `react-style.md`.

## Validation and states

<!-- rule id=user-facing-feedback/validate-inputs-allowed-state -->
- Validate inputs and the allowed state before running the action.
  - Block an invalid action instead of letting it fail silently.

<!-- rule id=user-facing-feedback/render-loading-success-empty -->
- Render loading, success, empty, and error explicitly and accessibly, close to the control that started the operation.

<!-- rule id=user-facing-feedback/keep-validation-state-operation -->
- Keep validation state, operation state, and any error tracking context separate.
  - Do not reuse one generic message for different states.

<!-- rule id=user-facing-feedback/clear-errormessage-validationmessage-error -->
- Clear `errorMessage`, `validationMessage`, any error tracking context, timers, listeners, and `AbortController`s when the resource, facility, access, or filter changes, when a modal closes or reopens, and when a new attempt or retry starts.

<!-- rule id=user-facing-feedback/show-error-previous-resource -->
- Never show an error from a previous resource while a new resource is loading or ready, and never let a previous result update a new selection.

## Incremental mutations

<!-- rule id=user-facing-feedback/prefer-incremental-responses-full -->
- Prefer incremental responses over full route refreshes: when the mutated UI can be updated from a safe result, the route handler or server action returns the minimum view model needed to update the affected state.

<!-- rule id=user-facing-feedback/refresh-whole-route-justified -->
- Refresh the whole route only when it is justified by broad cache invalidation, data that cannot be rebuilt safely from the result, a security or authorization change, or critical cross-view synchronization.
  - Document the reason next to the refresh.

<!-- rule id=user-facing-feedback/tests-user-triggered-mutations -->
- Tests for user-triggered mutations assert the observable outcome of an incremental update: the affected UI shows the result while unrelated state (form input, scroll, focus, open panels) is preserved.
  - Do not assert on calls to framework refresh helpers.
  - Cover the whole-route behavior in an integration or end-to-end test when it matters.

## Async feedback and error tracking

<!-- rule id=user-facing-feedback/toast-notification-component-project -->
- Use the toast or notification component of the project's UI library (for example `toast` from `@golfo/ui`, backed by Sonner) for async feedback: loading, success, information, expected warnings, and recoverable errors.
  - Prefer its promise helper (for example `toast.promise`) for write operations so loading, success, and failure share one lifecycle.
  - Mount the project's toaster once, as its conventions define.
  - Never mount a second one or restyle toasts locally.

<!-- rule id=user-facing-feedback/inline-messages-next-control -->
- Use inline messages next to the control (not toasts) for local validation, empty lists, and valid business states.
  - A degraded but valid response (for example a `202` with pending requirements) keeps its status and stays a business state, not a technical error.

<!-- rule id=user-facing-feedback/wire-error-tracking-feedback -->
- Wire an error tracking feedback component (for example one tied to the project's error monitoring tool) only when the project has one, a real error tracking context exists, and the failure is actionable or unexpected and needs tracking.
  - Never fabricate a context from the component.
  - Without one, show a safe visual fallback.
  - Do not add an error monitoring tool only to satisfy this rule.

<!-- rule id=user-facing-feedback/enable-retry-safe-idempotent -->
- Enable retry only when it is safe or idempotent, or resumes known progress.
  - A retry must never create a duplicate mutation.

<!-- rule id=user-facing-feedback/keep-public-message-short -->
- Keep the public message short, localized, and separate from the technical detail.

<!-- rule id=user-facing-feedback/detail-include-operation-stage -->
- The detail may include operation, stage, category, code, dependency, status, counts, and opaque stable identifiers (`userId`, `requestId`, correlation or `traceId`, resource ids).
  - Never include the raw condition, upstream payload, full request or response, headers, cookies, tokens, secrets, or PII (emails, phone numbers, names) in the detail, logs, DTOs, or test assertions.

## Accessibility

<!-- rule id=user-facing-feedback/associate-feedback-affected-control -->
- Associate feedback with the affected control or region.

<!-- rule id=user-facing-feedback/suitable-roles-live-regions -->
- Use suitable roles and live regions without announcing the same error twice.

<!-- rule id=user-facing-feedback/keep-focus-close-retry -->
- Keep focus, close, and retry usable from the keyboard.

## Tests

<!-- rule id=user-facing-feedback/cover-happy-path-error -->
- Cover happy path, error, loading, empty, retry, cancellation, and partial states when the flow has them.

<!-- rule id=user-facing-feedback/async-feedback-cover-toast -->
- For async feedback, cover the toast or notification shown for each outcome (loading, success, failure) through what the user sees, rendering the project's real toaster instead of mocking the UI library.

<!-- rule id=user-facing-feedback/project-has-error-tracking -->
- When the project has an error tracking feedback component, also cover: valid error tracking context, unexpected error without retry, fallback without context, stale-state cleanup, and no error tracking feedback in expected states.

<!-- rule id=user-facing-feedback/test-logs-part-explicit -->
- Test logs only when they are part of an explicit contract.
  - Prefer asserting the public projection and the sanitized detail.
