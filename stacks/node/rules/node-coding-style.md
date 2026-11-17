# Coding Style Rules — Node

<!-- rule id=node-coding-style/follow-linter-formatter-project -->
- Follow the linter and formatter the project already configures.
  - Do not reformat unrelated code.

<!-- rule id=node-coding-style/async-await-handle-rejection -->
- Use `async`/`await` and handle every rejection: no floating promises, and no mixing of callbacks and promises in the same flow.

<!-- rule id=node-coding-style/run-independent-async-work -->
- Run independent async work concurrently with `Promise.all` or `Promise.allSettled` instead of a sequential `await` inside a loop.

<!-- rule id=node-coding-style/block-event-loop-synchronous -->
- Never block the event loop with synchronous I/O (`fs.*Sync`, `child_process.*Sync`) or CPU-heavy work in request handlers.

<!-- rule id=node-coding-style/read-configuration-environment-variables -->
- Read configuration from environment variables once, validated at startup, in a dedicated config module.
  - Do not read `process.env` throughout the code.

<!-- rule id=node-coding-style/keep-route-handlers-thin -->
- Keep route handlers thin: validate input, delegate to a service, and map the result to the response.

<!-- rule id=node-coding-style/give-outbound-http-call -->
- Give every outbound HTTP call a timeout and propagate cancellation (`AbortSignal`) when the caller can abort.
