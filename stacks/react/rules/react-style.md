# React Style Rules — React + TypeScript

Coding conventions for this stack. Always consult the documentation of the project's framework and design system for their APIs before implementing — these rules cover conventions, not API details.

---

## Components

<!-- rule id=react-style/function-components-hooks-class -->
- Use function components with hooks — no class components.

<!-- rule id=react-style/keep-components-small-single -->
- Keep components small and single-responsibility.
  - Extract when a component has more than one reason to change.

<!-- rule id=react-style/extract-complex-logic-custom -->
- Extract complex logic into custom hooks (`use<Name>`).

<!-- rule id=react-style/useeffect-derive-state-see -->
- Do not use `useEffect` to derive state.
  - See `Security and UI` in `patterns-we-do-not-use.md`.

<!-- rule id=react-style/avoid-prop-drilling-beyond -->
- Avoid prop drilling beyond two levels — use context or a state manager.

<!-- rule id=react-style/rest-props-rest-declare -->
- Never use rest props (`...rest`) — declare all props explicitly.

<!-- rule id=react-style/one-component-file-export -->
- **One component per file** — never export more than one component from a single file.
  - A file named `user-card.tsx` exports only `UserCard`.

<!-- rule id=react-style/component-placement-follow-component -->
- **Component placement** — follow the component locations declared in the project's `AGENTS.md` (or its architecture docs).
  - When the project declares none, use `components/<scope>/<component-name>/` (or `src/components/<scope>/<component-name>/` when the project keeps code under `src/`), where `<scope>` groups components by feature or domain and shared primitives use a generic scope such as `common`.
  - Never place components inside a file-system router's routes directory: it only holds the framework's route files. Pages import components from the component location.
  - Do not add barrel files (`index.ts` that re-export many components) unless the project already uses them; import each component from its own folder.

<!-- rule id=react-style/atomic-size-keep-components -->
- **Atomic size** — keep components at the smallest meaningful unit.
  - A component that mixes concerns (layout + data formatting + interaction) must be split.

## Design system

<!-- rule id=react-style/project-s-design-system -->
- Use the project's design system components for all UI elements: buttons, inputs, modals, selects, etc.

<!-- rule id=react-style/build-custom-replacements-components -->
- Never build custom replacements for components the design system already provides.

<!-- rule id=react-style/design-system-props-example -->
- Use design system props (for example `variant`, `size`, `color`) to control appearance before adding any custom CSS.

<!-- rule id=react-style/add-custom-css-design -->
- Only add custom CSS when the design system has no prop or component that covers the need.

<!-- rule id=react-style/override-internal-design-system -->
- Never override internal design system component styles with custom CSS.

<!-- rule id=react-style/custom-styles-needed-write -->
- When custom styles are needed, write them with the project's styling solution (for example SCSS/Sass Modules or Tailwind, whichever the project already uses) and the design system tokens.
  - Never hardcode colors, typography, spacing, breakpoints, radius, or elevation.

<!-- rule id=react-style/project-s-image-component -->
- Use the project's image component or provider for images, icons, and backgrounds with relative or environment-dependent paths.
  - Keep lazy loading and avoid absolute URLs.

<!-- rule id=react-style/consult-design-system-documentation -->
- Always consult the design system documentation before selecting a component.

## User-facing copy

<!-- rule id=react-style/project-already-i18n-library -->
- When the project already uses an i18n library (gettext, next-intl, i18next, react-intl, or similar), route every visible React string through its translation function.
  - Visible strings include labels, buttons, placeholders, helper and error text, toasts, and aria labels.
  - The translation function is, for example, `i18n.gettext`, `useTranslations`, or `t`.
  - Reuse existing message ids before creating new ones, and do not hand-edit catalogs that the i18n workflow generates.

<!-- rule id=react-style/project-has-i18n-library -->
- When the project has no i18n library, do not add one only to satisfy this rule: write user-facing copy in the language set by the project's language policy (`AGENTS.md`), keep it in the component as the framework expects, and name only the copy identifiers or keys that carry behavior.

<!-- rule id=react-style/write-labels-buttons-headings -->
- Write labels, buttons, headings, helper text, empty states, confirmations, and progress messages for people who use the product, not for the team that built it.

<!-- rule id=react-style/avoid-unnecessary-secondary-labels -->
- Avoid unnecessary secondary labels and descriptions.
  - Let the design do the explaining: before adding a subtitle, helper text, tagline, or explanatory paragraph, resolve the ambiguity with layout, hierarchy, grouping, a clearer primary label, an icon, or the design system's affordances.
  - Do not write slogan-like headings or copy that turns the interface into an instruction manual.
  - This does not remove accessible names (`aria-label`, visually hidden labels), validation and error messages, or text that states a consequence the user needs before acting (for example an irreversible deletion).

<!-- rule id=react-style/avoid-implementation-terms-regular -->
- Avoid implementation terms in regular UI copy, including `preflight`, `bootstrap`, `provider`, `stack`, `upstream`, `lockfile`, `schema`, `sync`, and `retry` when they describe internal mechanics.
  - Prefer the user-visible action or outcome, such as `Reintentar` instead of `Reintentar preflight`.

<!-- rule id=react-style/expose-internal-component-names -->
- Do not expose internal component names, service names, workflow names, file names, status codes, or infrastructure details in regular UI copy.
  - Keep those details in logs or technical documentation, not in ordinary interface text.

<!-- rule id=react-style/keep-error-messages-clear -->
- Keep error messages clear and actionable.
  - Errors may include the minimum technical detail needed to diagnose or resolve the problem, but never expose secrets or unnecessary internal data.

<!-- rule id=react-style/review-new-changed-user -->
- Review every new or changed user-facing string from the perspective of a non-technical user.
  - If the message explains how the system works instead of what the user can do or expect, rewrite it.

## TypeScript

<!-- rule id=react-style/type-props-explicitly -->
- Always type props explicitly — no `any`.

<!-- rule id=react-style/interface-object-shapes-type -->
- Use `interface` for object shapes.
  - `type` for unions and aliases.

<!-- rule id=react-style/enum-const-objects-const -->
- Never use `enum` — use `const` objects with `as const` or string union types.

<!-- rule id=react-style/parameter-properties-classes -->
- Never use parameter properties in classes.

<!-- rule id=react-style/closing-change-run-project -->
- Before closing the change, run the project's own typecheck and lint scripts from `package.json` (for example `typecheck`, `lint`, or the `ci` script that bundles them) instead of ad hoc commands such as a bare `tsc --noEmit`.
  - Fix every reported error.
  - When one of those scripts does not exist, report that check as `N/A` instead of substituting a direct binary.
  - Run them once at the end of the task, as `verify-changes.md` and `lint-gate.md` define, not after every file.

## Function parameters

<!-- rule id=react-style/boolean-parameters-switch-function -->
- Never use boolean parameters to switch a function's behavior.
  - A call like `getItems(locale, true, true)` is unreadable at the call site, is easy to call with arguments in the wrong order, and every extra flag doubles the hidden combinations, including invalid ones.

<!-- rule id=react-style/semantic-string-names-state -->
- Use a semantic string that names the state or mode instead.
  - When several flags describe one state, collapse them into a single value that only allows valid combinations:

  ```ts
  // ❌ What do `true, true` mean? Is `featuredOnly` without `activeOnly` valid?
  function getItems(locale: string, activeOnly = false, featuredOnly = false) {}
  getItems(locale, true, true);

  // ✅ The call reads as intent and invalid combinations cannot be expressed
  type ItemListScope = 'all' | 'active' | 'active-featured';

  function getItems(locale: string, scope: ItemListScope = 'all') {}
  getItems(locale, 'active-featured');
  ```

<!-- rule id=react-style/declare-allowed-values-string -->
- Declare the allowed values as a string union type, or as an `as const` object in `constants/` when the values are reused across modules.
  - Never use `enum` (see TypeScript).

<!-- rule id=react-style/replacing-existing-boolean-parameter -->
- When replacing an existing boolean parameter, update every call site in the same change.
  - Do not keep the boolean and the string side by side.

<!-- rule id=react-style/rule-covers-parameters-select -->
- This rule covers parameters that select behavior.
  - Boolean props that follow design system or DOM conventions (`disabled`, `checked`, `open`), predicate return values, and boolean fields that come from an upstream payload stay boolean.

## Naming

| Entity | Convention | Example |
|--------|-----------|---------|
| Components | PascalCase | `UserProfile` |
| Hooks | camelCase with `use` prefix | `useUserProfile` |
| Files & directories | kebab-case | `user-profile.tsx` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRIES` |
| Functions & variables | camelCase | `getUserProfile` |

## Module placement

<!-- rule id=react-style/follow-module-layout-declared -->
- Follow the module layout declared in the project's `AGENTS.md` or architecture docs (for example `src/modules/<feature>/{domain,application,infrastructure}`) before applying the defaults below.

<!-- rule id=react-style/keep-route-entrypoints-route -->
- Keep route entrypoints (route handlers, server actions, pages) focused on validation at the boundary, orchestration, and calls to use cases or services.
  - Do not add shared utilities or reusable constants inside them.

<!-- rule id=react-style/projects-without-feature-modules -->
- In projects without feature modules, place shared or reusable utility functions in `utils/` and domain/configuration constants in `constants/`.
  - With feature modules, keep them in the owning module (`src/modules/<feature>/constants/`, or `src/modules/shared/...` when several modules reuse them) (see `hexagonal-architecture.md` in Next.js projects).
  - Extract anything reused or carrying domain meaning.

## Performance

<!-- rule id=react-style/avoid-unnecessary-object-cloning -->
- Avoid unnecessary object cloning with spread — pass objects directly when no mutation is needed.

<!-- rule id=react-style/react-memo-usememo-usecallback -->
- Use `React.memo`, `useMemo`, and `useCallback` only when profiling confirms a render bottleneck — not preemptively.
  - When it does, stabilize the handlers passed to memoized children with `useCallback` instead of inline functions.

<!-- rule id=react-style/lazy-load-routes-heavy -->
- Lazy-load routes and heavy components.

## Imports

<!-- rule id=react-style/project-s-ssr-framework -->
- When the project's SSR framework re-exports a package, import it from the framework's re-export — never from the underlying package directly.

<!-- rule id=react-style/install-packages-ssr-framework -->
- Never install packages that the SSR framework already bundles (for example `react` or `react-dom`).

<!-- rule id=react-style/check-framework-s-package -->
- Check the framework's `package.json` in `node_modules/` before installing any new dependency.

<!-- rule id=react-style/lodash-es-availability-mandatory -->
- For `lodash-es` availability, mandatory and forbidden methods, see `lodash.md`.

## Logging

<!-- rule id=react-style/project-s-logger-console -->
- Use the project's logger.
  - Never use `console.*` in application code.

<!-- rule id=react-style/write-log-message-operation -->
- Write each log message with operation, stage, outcome, code, and safe context.
  - Opaque, stable identifiers (`userId`, `requestId`, `traceId`, resource ids) are allowed and encouraged for diagnosis.
  - Never log PII (emails, phone numbers, names, addresses), raw request or response payloads, tokens, cookies, or secrets (see `Secrets & PII` in `react-security.md`).

## Comments

<!-- rule id=react-style/comment-why-well-named -->
- Comment the WHY, not the WHAT.
  - Well-named identifiers explain themselves.

<!-- rule id=react-style/add-inline-comments-non -->
- Only add inline comments for non-obvious constraints, workarounds, or invariants.

<!-- rule id=react-style/document-exported-components-hooks -->
- Document exported components, hooks, functions, and types with JSDoc/TSDoc when their intent, contract, or complexity is not evident from the signature (props with non-obvious behavior, side effects, thrown errors, invariants).
  - Follow the `enforce-jsdoc-tsdoc` skill when it is available.
  - Do not add JSDoc that only restates the name or the types.
