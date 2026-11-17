# Security Rules — Android

<!-- rule id=android-security/treat-everything-apk-public -->
- Treat everything in the APK as public: `BuildConfig` fields, resources, assets, and code can all be extracted, and R8 does not hide them.
  - Keep secrets on a server the app authenticates against.
  - Keep build-time keys in `local.properties` or the CI secret store, never in the repository.

<!-- rule id=android-security/store-tokens-other-sensitive -->
- Store tokens and other sensitive data encrypted with a key held in the Android Keystore.
  - Never in plain `SharedPreferences`, external storage, or logs.
  - Exclude that data from backups (`android:dataExtractionRules`, `android:fullBackupContent`).

<!-- rule id=android-security/https-keep-cleartext-traffic -->
- Use HTTPS only and keep cleartext traffic disabled in the network security config.
  - Never ship a custom `TrustManager` or `HostnameVerifier` that accepts everything, not even behind a debug flag that could reach a release build.

<!-- rule id=android-security/set-android-exported-false -->
- Set `android:exported="false"` on every component that other apps do not need.
  - Treat every `Intent` extra, deep link, and `ContentProvider` argument as untrusted input: validate it before using it to navigate, load a URL, or open a file.

<!-- rule id=android-security/explicit-intents-internal-communication -->
- Use explicit intents for internal communication, and `FLAG_IMMUTABLE` on a `PendingIntent` unless it must be mutable.

<!-- rule id=android-security/keep-javascript-disabled-webview -->
- Keep JavaScript disabled in a `WebView` unless the screen needs it, load only allowlisted origins, disable file access, and expose `addJavascriptInterface` only to content you control.

<!-- rule id=android-security/parameterized-queries-room-query -->
- Use parameterized queries (Room `@Query` parameters, selection arguments).
  - Never concatenate user input into SQL.

<!-- rule id=android-security/share-files-through-fileprovider -->
- Share files through `FileProvider`, never `file://` URIs, and validate entry names when extracting an archive so a path cannot escape the target directory.

<!-- rule id=android-security/request-runtime-permissions-feature -->
- Request only the runtime permissions a feature needs, at the moment it needs them, and keep the feature usable or clearly degraded when the user denies them.

<!-- rule id=android-security/enforce-authorization-server-check -->
- Enforce authorization on the server.
  - A check in the app only shapes the UI, because a modified client can skip it.

<!-- rule id=android-security/keep-release-builds-non -->
- Keep release builds non-debuggable and with R8 enabled.
  - Show safe error messages to users, and log failures as `error-handling.md` › `Diagnosable failures` defines.
  - Never log tokens, personal data, or full request bodies.

<!-- rule id=android-security/scan-dependencies-change-example -->
- Scan dependencies when they change (for example with Dependabot or OWASP Dependency-Check, whichever the project uses) and resolve reported vulnerabilities.
