## Why

The frontend currently uses eager component loading and lacks consistent Signal-based form state management in the login-register screen. This misalignment blocks the next phase (backend/Supabase integration) and makes the codebase harder to maintain. A refactor now ensures all components follow the same established conventions before the scope expands.

## What Changes

- Migrate all routes from eager `component:` imports to lazy `loadComponent()` calls in `app.routes.ts`
- Add Bootstrap 5 CDN link to `src/index.html` (required but never added)
- Refactor `login-register` to use `signal({...})` for form fields + `computed()` for validations (currently fields are unbound)
- Remove the 10 eager imports from `app.routes.ts` (they move into inline `import()` calls)
- No visual changes except what Bootstrap CDN enables (no design regressions)
- Verify with `npm run build`

## Capabilities

### New Capabilities

- `frontend-refactor-align`: Enforce Angular project conventions — lazy loading, Bootstrap CDN, and Signal-based form state — as a single cross-cutting change. No new user-facing features.

### Modified Capabilities

- *(None — requirements remain identical; only implementation details change)*

## Impact

- **`servihogar-frontend/src/app/app.routes.ts`** — rewrite all 11 route definitions
- **`servihogar-frontend/src/index.html`** — add Bootstrap CDN `<link>` and `<script>`
- **`servihogar-frontend/src/app/components/login-register/login-register.ts`** — add form signal + computed validations
- **`servihogar-frontend/src/app/components/login-register/login-register.html`** — bind inputs to signal fields and disable/enable submit button
- No changes to backend, database, or other frontend components
