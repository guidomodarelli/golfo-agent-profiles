# Established Libraries

Prefer an established, well-maintained library over a custom implementation when it solves the need.

<!-- rule id=established-libraries/writing-utility-parser-validator -->
- Before writing a utility, parser, validator, date or number handling, retry logic, or any other general-purpose mechanism, check whether a dependency already declared in the project, or shipped by its framework, covers it.
  - Reuse it with its supported API.

<!-- rule id=established-libraries/add-dependency-standard-library -->
- Do not add a dependency for what the standard library or the framework already covers.
  - See `Architecture and dependencies` in `patterns-we-do-not-use.md`.

<!-- rule id=established-libraries/declared-dependency-covers-need -->
- When no declared dependency covers the need, prefer a widely adopted library with active maintenance, recent releases, and a compatible license over hand-rolling the behavior.

<!-- rule id=established-libraries/install-new-library-without -->
- Never install a new library without asking first, including dev dependencies and libraries a skill's preflight would otherwise add (for example `express`, `zod`, `pino`, `axios`, `config`, `nock`).
  - State the library, the need it covers, and the alternative already in the project (or that there is none), then wait for the user's confirmation before adding it.
  - If the user declines, use the existing alternative or stop and report what is missing.

<!-- rule id=established-libraries/type-package-library-being -->
- A type package for the library being added (for example `@types/express`) is part of the same question.
  - Do not ask for it separately.

<!-- rule id=established-libraries/project-already-has-equivalent -->
- When the project already has an equivalent (for example, a validation library other than the one a skill shows, or an existing logger), reuse it instead of proposing a second library for the same need.

<!-- rule id=established-libraries/moving-library-already-declared -->
- Moving a library that is already declared from `devDependencies` to `dependencies` because production code imports it is not a new library.
  - Do it and mention it in the change summary.

<!-- rule id=established-libraries/exception-lodash-es-stacks -->
- Exception: `lodash-es` in stacks that ship `lodash.md`.
  - That rule makes `lodash-es` mandatory, so installing it (and `@types/lodash-es`) when it is not declared is pre-approved.
  - Follow `lodash.md`.
  - No other library is pre-approved.

<!-- rule id=established-libraries/stack-rules-name-specific -->
- Stack rules that name a specific library or its availability order take precedence over this rule only for choosing which declared library to reuse, never to skip the confirmation.
