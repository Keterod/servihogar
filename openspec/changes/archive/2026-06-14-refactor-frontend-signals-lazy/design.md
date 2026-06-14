## Context

The frontend was built incrementally as a prototype. Routes import components eagerly (`component: ComponentName`), Bootstrap was never wired via CDN, and the `login-register` component has unbound form inputs with no Signal state. The project conventions (AGENTS.md) mandate lazy loading, Bootstrap CDN, and Signal-based form state — but the code has not been updated to reflect them.

This change is purely a refactor: no new features, no visual changes, no backend/database modifications.

## Goals / Non-Goals

**Goals:**
- Replace all eager `component:` route entries with `loadComponent: () => import(...)`
- Add Bootstrap 5 CSS/JS CDN links to `src/index.html`
- Refactor `login-register` to use `signal({...})` for form fields and `computed()` for validation (submit disabled when fields are empty)
- Verify the build compiles without errors (`npm run build`)

**Non-Goals:**
- No new features, screens, or APIs
- No visual redesign — CSS changes only what Bootstrap CDN enables
- No backend or Supabase integration
- No database schema changes
- No modification of other components' existing Signal patterns (they are already compliant)
- No migration of existing components from individual signals to single-form signals (leave `solicitud-servicio`, `valorar-servicio`, `panel-tecnico`, `panel-administrador` as-is)

## Decisions

1. **`loadComponent` over `loadChildren` or `loadComponent` with modules** — All components are standalone, so `loadComponent` is the idiomatic Angular 15+ approach. No lazy-loaded module wrappers needed.

2. **Bootstrap 5.3 via CDN** — Use the latest stable Bootstrap 5.3.x from CDN (jsDelivr). This matches the "Bootstrap via CDN only" constraint in AGENTS.md. The `<link>` goes in `<head>`, scripts at end of `<body>`.

3. **Single `signal({...})` for login-register** — Consolidate all form fields (nombre, email, password, confirmPassword, especialidad, zona, telefono) into a single form signal, mirroring the pattern in `panel-tecnico` and `panel-administrador`. This is cleaner than individual signals for each field.

4. **No spec delta files** — No requirements are changing (the same screens behave identically from the user's perspective). Only implementation details change. The single spec for `frontend-refactor-align` covers the non-functional requirements.

## Risks / Trade-offs

- **[Low] Login-register refactor adds fields that are not yet validated visibly** — Mitigation: `computed()` for `puedeEnviar` will disable the submit button until required fields are filled. A "Prototipo académico" note already exists.
- **[Low] Build fails if a component uses Node.js built-ins or missing imports** — Mitigation: Run `npm run build` after each logical group of changes and fix incrementally.
