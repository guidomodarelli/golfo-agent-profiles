---
trigger: always_on
---

# Environment Readiness

A missing configuration value or an outdated local database must show up when the app starts, not as a server error in the middle of a flow.

## Environment variables

<!-- rule id=environment-readiness/environment-variable-feature-reads -->
- Add every environment variable a feature reads, in the same change, to the project's example environment file and to a single startup requirements registry.
  - The registry names the feature that needs it and a severity: `blocking` when the feature cannot work without it, `degraded` when the feature turns itself off.

<!-- rule id=environment-readiness/present-value-still-unusable -->
- When a present value can still be unusable (JSON, keys, URLs, enums), the requirement validates it with the same parser the feature uses at runtime, so a malformed value fails at startup too.

<!-- rule id=environment-readiness/startup-check-logs-unmet -->
- The startup check logs every unmet requirement with the feature, the variable names, and the validation's error types and codes.
  - Never values.
  - In local development a blocking requirement stops the app before any flow runs.
  - In production the check only logs: the affected feature keeps failing closed on its own, and the log says why.

<!-- rule id=environment-readiness/skip-check-during-builds -->
- Skip the check during builds that run without runtime secrets.

<!-- rule id=environment-readiness/paper-missing-variable-hardcoded -->
- Do not paper over a missing variable with a hardcoded fallback.

## Local database

<!-- rule id=environment-readiness/local-development-start-command -->
- The local development start command warns when the configured database lacks versioned migrations from the repository, naming the database host and the pending migrations.
  - It never blocks startup when the check itself cannot run.
  - It says why.

<!-- rule id=environment-readiness/apply-pending-migrations-developer -->
- Apply pending migrations on the developer's own disposable database (a personal branch or local instance) before testing a flow by hand, following `database.md` for where migrations may run.

<!-- rule id=environment-readiness/feature-needs-local-secrets -->
- When a feature needs local secrets or enrolled key material to work (signing keys, encryption keyrings), make the command that prepares the local database generate development-only values when they are missing.
  - It stores them only in a git-ignored local environment file and enrolls them in that same local database.
  - Never reuse those values in another environment.
