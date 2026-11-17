# Database Rules

Applies to projects that talk to a relational database. If the project has no database, this rule does not apply.

## Schema changes

<!-- rule id=database/change-database-structure-schema -->
- Ship every change to database structure with a versioned migration in the same task.
  - Database structure means the schema, tables, columns, constraints, indexes, relationships, or row-level security.
  - Write the migration in the format the project's migration tool runs (SQL files, or framework-native migrations such as TypeORM, Liquibase, or Django).
  - A dashboard SQL editor is for experiments only and never replaces the migration.

<!-- rule id=database/edit-migration-have-been -->
- Do not edit a migration that may have been applied.
  - See `Data` in `patterns-we-do-not-use.md`.

<!-- rule id=database/store-money-floating-point -->
- Do not store money in floating-point columns or persist local timestamps.
  - See `Data` in `patterns-we-do-not-use.md`.

<!-- rule id=database/validate-migrations-sql-functions -->
- Validate migrations, SQL functions, and policies on a disposable database (an ephemeral branch or a local Postgres) before closing the task.
  - Run the committed migration through the project's configured migrator (or, for SQL files, the committed SQL as written), not an ad-hoc rewrite.
  - When fixing a bug, reproduce the failing case first.

<!-- rule id=database/experiment-seed-mutate-default -->
- Never experiment on, seed, or mutate the default or production database.
  - Applying migrations there needs an explicit request.

<!-- rule id=database/print-persist-secrets-connection -->
- Never print or persist secrets, connection strings, or sensitive row data while debugging.
  - Prefer metadata queries.

## Pooled connections

The examples use Node.js and `pg`; apply the same guarantees with your stack's pool.

<!-- rule id=database/pooled-client-leaks-code -->
- A pooled client leaks when the code holding it never reaches its release: an `await` that never settles (a hung query or socket after the request or render was aborted), or an execution context torn down mid-flight.
  - Leaked clients exhaust the pool.
  - A fast direct connection with pool `timeout exceeded` errors means pool starvation, not a slow database.

<!-- rule id=database/path-checks-out-pooled -->
- Release every pooled client a path checks out, even when the request or render that started it is cancelled.
  - Tie the checkout to the cancellation signal the framework provides (for example an `AbortSignal`) and destroy the client when it fires.
  - Register a client `error` listener that destroys the client when its socket fails.
  - Guard against double release, and never issue `ROLLBACK` on a socket that already errored.
  - Reuse the project's safe checkout helper instead of writing a new bare `connect()`/`finally` pair.

<!-- rule id=database/give-request-scoped-transactions -->
- Give request-scoped transactions a server-side idle timeout, far larger than any legitimate transaction, so the server reclaims abandoned ones.
  - In PostgreSQL, set a local `idle_in_transaction_session_timeout` right after `BEGIN`, and apply the same guard per connection (for example in the pool's connect hook) to cover transactions opened by libraries that own their checkout.
  - On other databases, use their equivalent setting when one exists, and otherwise rely on the release guarantees above.

<!-- rule id=database/size-pool-max-concurrent -->
- Size the pool `max` for concurrent requests and renders.

<!-- rule id=database/retry-connection-acquisition-timeouts -->
- Do not retry connection-acquisition timeouts: retrying while the pool is saturated doubles the pressure.
  - Retry only genuinely transient terminations, such as a backend-closed idle client.

<!-- rule id=database/run-provider-call-plus -->
- Do not run a provider call plus a write on every server-rendered read.
  - Throttle reconciliation behind a freshness window.

<!-- rule id=database/closing-task-touches-database -->
- Before closing a task that touches database access, transactions, pools, retries, or provider calls on a render path, search the codebase for the same pattern.
  - The pattern includes `pool.connect()`, pool factories, request-scoped transactions and retry helpers.
  - Confirm every occurrence follows these rules, or record why it is exempt.
