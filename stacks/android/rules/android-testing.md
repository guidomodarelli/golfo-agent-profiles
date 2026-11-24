---
trigger: always_on
---

# Testing Rules — Android

<!-- rule id=android-testing/put-tests-need-device -->
- Put tests that do not need a device in `src/test` (local JVM) and keep `src/androidTest` for what really needs one: real UI, framework behavior, or the database on a device.
  - Name tests after the behavior they verify.

<!-- rule id=android-testing/test-framework-assertion-library -->
- Use the test framework and assertion library the project already uses.
  - Run the local suite with `./gradlew test` and the device suite with `./gradlew connectedAndroidTest`.

<!-- rule id=android-testing/test-viewmodels-asserting-ui -->
- Test ViewModels by asserting the UI state they expose, with `runTest` and an injected test dispatcher.
  - Never use `Thread.sleep`.

<!-- rule id=android-testing/prefer-fakes-boundaries-project -->
- Prefer fakes at the boundaries the project owns (repositories, data sources, outbound clients).
  - Do not mock the Android framework, Kotlin coroutines, or value objects.
  - Use Robolectric or a device test when framework behavior matters.

<!-- rule id=android-testing/test-compose-ui-through -->
- Test Compose UI through its semantics (`onNodeWithText`, `onNodeWithContentDescription`), and add a `testTag` only when no user-visible property identifies the node.
  - Wait with `waitUntil` or an idling resource, not with a fixed delay.

<!-- rule id=android-testing/test-room-queries-against -->
- Test Room queries against a real in-memory Room database, and every schema change with `MigrationTestHelper`, so a migration that loses data fails before release.

<!-- rule id=android-testing/mock-own-database-layer -->
- Do not mock your own database layer in integration tests.
  - See `Data` in `patterns-we-do-not-use.md`.
