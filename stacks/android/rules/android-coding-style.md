# Coding Style Rules — Android

<!-- rule id=android-coding-style/follow-formatter-static-analysis -->
- Follow the formatter and static analysis the build already configures (for example ktlint, detekt, or Android Lint).
  - Do not reformat unrelated code or add a baseline to hide new lint errors.

<!-- rule id=android-coding-style/write-new-code-kotlin -->
- Write new code in Kotlin unless the module is still Java only.

<!-- rule id=android-coding-style/keep-business-logic-out -->
- Keep business logic out of Activities, Fragments, and composables: they render state and forward events.
  - A ViewModel exposes one immutable `StateFlow` of UI state and calls the data layer.

<!-- rule id=android-coding-style/hold-activity-fragment-view -->
- Do not hold an Activity, Fragment, View, or their `Context` in a ViewModel, a singleton, or a static field.
  - It leaks the whole screen.
  - Use the application context when a context must outlive a screen.

<!-- rule id=android-coding-style/keep-state-survive-process -->
- Keep state that must survive process death in `SavedStateHandle` or persistent storage.
  - Surviving a rotation is not enough.

<!-- rule id=android-coding-style/launch-coroutines-viewmodelscope-lifecyclescope -->
- Launch coroutines from `viewModelScope` or `lifecycleScope`, never `GlobalScope`.
  - Collect flows with lifecycle awareness (`collectAsStateWithLifecycle` or `repeatOnLifecycle`), so nothing keeps collecting in the background.

<!-- rule id=android-coding-style/blocking-i-o-off -->
- Do blocking I/O off the main thread.
  - Make suspending functions main-safe, and inject dispatchers instead of hardcoding `Dispatchers.IO`, so tests can control them.
  - Rethrow `CancellationException` when catching broad exceptions.

<!-- rule id=android-coding-style/compose-hoist-state-caller -->
- In Compose, hoist state to the caller and pass values and lambdas instead of a ViewModel.
  - Keep composables free of side effects outside `LaunchedEffect` and its siblings, and give lazy list items a stable `key`.

<!-- rule id=android-coding-style/put-user-visible-text -->
- Put user-visible text in string resources, with plurals where needed, and give interactive elements without visible text a content description.

<!-- rule id=android-coding-style/declare-dependencies-version-catalog -->
- Declare dependencies in the version catalog when the project has one, and raise `minSdk` or `targetSdk` only as a deliberate change.
