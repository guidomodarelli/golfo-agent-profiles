---
trigger: always_on
---

# Cross-Engine Compatibility — Chromium and WebKit

Every style and every piece of client-side JavaScript must render and behave correctly on Chromium (Chrome, Edge, Android Chrome) and WebKit (Safari, iOS Safari, iOS Chrome, iOS WebViews). Verify on both engines when both are available; the managed browser tooling only installs Chromium, so see `Verification` for how to close a task when WebKit cannot be exercised.

## Styles

<!-- rule id=cross-engine/validate-small-viewports-both -->
- Validate small viewports on both engines: several divergences only appear on mobile Chrome and iOS.

<!-- rule id=cross-engine/careful-layout-features-whose -->
- Be careful with layout features whose sizing differs between engines.
  - They include grid `fr`/`minmax()` tracks inside `fit-content` or `auto` containers, `-webkit-line-clamp` with `-webkit-box`, flex and grid `min-height`/`min-width` defaults, sticky positioning, fixed positioning combined with `inset` or `margin: auto`, and viewport units.
  - When a scroll container depends on an `fr` track, give it a definite size.

<!-- rule id=cross-engine/keep-required-webkit-prefixes -->
- Keep the required `-webkit-` prefixes and provide a standard fallback.
  - Never ship a property or value only one engine understands.

## Viewport units

<!-- rule id=cross-engine/svh-page-section-min -->
- Use `svh` for page or section `min-height` and for viewport-bound scroll containers.

<!-- rule id=cross-engine/dvh-fullscreen-mobile-overlays -->
- Use `dvh` only for fullscreen mobile overlays.

<!-- rule id=cross-engine/bare-100vh-swap-svh -->
- Do not use bare `100vh`, and never swap every `svh` for `dvh` in bulk.

## JavaScript

<!-- rule id=cross-engine/depend-chromium-apis-behaviors -->
- Do not depend on Chromium-only APIs or behaviors.
  - Guard non-universal Web APIs with feature detection and give WebKit a working fallback.

## Verification

<!-- rule id=cross-engine/fixing-reviewing-ui-bug -->
- When fixing or reviewing a UI bug, rule out an engine-specific cause and verify the fix on both engines.

<!-- rule id=cross-engine/one-engine-cannot-exercised -->
- If one engine cannot be exercised (for example, no WebKit browser or device is available), the task can close after you verify on the available engine, review the change against the risky features listed above, and report the blocker and the validation you ran.
