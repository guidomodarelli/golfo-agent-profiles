---
trigger: always_on
---

# Browser Before User Questions

Before asking the user for information or manual browser work, check whether the active provider can retrieve it or complete the authorized task through an available browser capability. Apply this in Claude Code and Codex, across every stack.

<!-- rule id=browser-before-user-questions/discover-capabilities-exposed-current -->
- Discover capabilities exposed in the current session, including connected MCPs, plugins, skills, and built-in browser controls.
  - Use Chrome DevTools MCP when available and suitable.
  - Alternatives include Playwright MCP, an installed agent-browser skill, or provider-native browser/computer-use controls such as `cua`.
  - These are examples, not required installations or guaranteed tool names.
  - Inspect the actual tool interface and follow its documentation.

<!-- rule id=browser-before-user-questions/requesting-url-screenshot-copied -->
- Before requesting a URL, screenshot, copied page content, console output, network details, or manual reproduction, inspect relevant open tabs and project configuration.
  - Use the browser to navigate, inspect the rendered page, reproduce the issue, and collect the evidence needed to proceed.
  - Capture screenshots yourself when supported.
  - Prefer an existing authenticated session when relevant.

<!-- rule id=browser-before-user-questions/continue-autonomously-recoverable-facts -->
- Continue autonomously with recoverable facts and actions already authorized by the task.
  - If one browser capability fails, try another available, suitable capability before handing the work to the user.
  - Browser installation belongs to the authorized agent-ready-setup bootstrap.
  - This rule alone does not authorize installation or reconfiguration.
  - Do not repeat attempts without new evidence.

<!-- rule id=browser-before-user-questions/ask-concrete-blocker-remains -->
- Ask only when a concrete blocker remains: no usable browser access, authentication/MFA requiring the user, unavailable information, or a preference or authorization the task does not establish.
  - State what was attempted, the remaining blocker, and the minimum user input needed.
  - Never ask the user to repeat evidence already recovered.

<!-- rule id=browser-before-user-questions/browser-access-grant-additional -->
- Browser access does not grant additional authorization for external writes or bypass authentication, permission requirements, or an explicit user restriction on browsing.
  - Verify the result in the page or other observable evidence before reporting success.
