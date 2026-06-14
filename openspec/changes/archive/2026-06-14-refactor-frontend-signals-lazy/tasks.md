## 1. Bootstrap CDN

- [x] 1.1 Add Bootstrap 5 CSS `<link>` to `<head>` of `src/index.html`
- [x] 1.2 Add Bootstrap 5 JS `<script>` at end of `<body>` in `src/index.html`

## 2. Lazy Loading Routes

- [x] 2.1 Replace all 11 eager `component:` imports in `app.routes.ts` with inline `loadComponent: () => import(...).then(m => m.ComponentName)`
- [x] 2.2 Remove the 11 top-level `import { ... }` statements from `app.routes.ts`
- [x] 2.3 Run `npm run build` and fix any lazy import errors

## 3. Login-Register Signal Form

- [x] 3.1 Add `signal({...})` for form fields (nombre, email, password, confirmPassword, especialidad, zona, telefono) in `login-register.ts`
- [x] 3.2 Add `computed()` for `puedeEnviar` (email+password required; register mode also requires nombre and confirmPassword)
- [x] 3.3 Add update method(s) for each form field (use `update()` with spread)
- [x] 3.4 Bind inputs in `login-register.html` to signal fields and disable submit button with `puedeEnviar()`

## 4. Build Verification

- [x] 4.1 Run `npm run build` and confirm zero errors
- [x] 4.2 Verify no `angular.json` or `package.json` Bootstrap entries were added
