## Context

ServiHogar uses Supabase PostgreSQL with `usuarios.auth_user_id` linked to `auth.users`. The backend currently bypasses authentication on demo endpoints by hardcoding demo `auth_user_id` values in repositories. The frontend `/login` screen is visual-only with role tabs but no session. Demo Auth users already exist:

| Email | Expected role / behavior |
| --- | --- |
| `cliente.demo@servihogar.com` | Cliente → `/panel-cliente` |
| `tecnico.demo@servihogar.com` | Técnico validado → `/panel-tecnico` |
| `admin.demo@servihogar.com` | Administrador → `/panel-administrador` |
| `tecnico.pendiente@servihogar.com` | Técnico pendiente → blocked from validated technician panel |

Constraints: no schema/seed changes, no `.env` edits in this change, no service role in frontend, keep existing demo business endpoints, follow backend layering and Angular Signals conventions.

## Goals / Non-Goals

**Goals:**
- Enable real Supabase Auth login/logout in Angular with anon key only.
- Expose `GET /auth/me` to map a valid JWT to the internal ServiHogar profile and derived role.
- Protect role dashboards with basic guards and redirect unauthenticated users to `/login`.
- Redirect authenticated users to the correct panel based on role and technician validation state.
- Keep business data access through FastAPI.

**Non-Goals:**
- Migrating all existing demo endpoints to require auth.
- Public self-service registration with profile creation in Supabase + DB.
- Password reset, email verification flows, refresh-token hardening, or RLS policy redesign.
- Removing footer demo links in this change (optional follow-up).
- Modifying `database/schema.sql`, `database/seed.sql`, or backend `.env`.

## Decisions

### 1. Frontend auth via `@supabase/supabase-js` with anon key only

Use the official Supabase JS client configured from a new frontend env module (e.g. `src/app/supabase.env.ts`) alongside existing `env.ts`. Store only `SUPABASE_URL` and `SUPABASE_ANON_KEY` (or publishable key). Never import service role.

**Alternative considered:** Custom REST calls to Supabase Auth endpoints. Rejected because the SDK handles session persistence and token refresh consistently.

### 2. Backend token validation with Supabase Auth `get_user(jwt)`

In `AuthService`, extract Bearer token from `Authorization` header. Validate using the existing backend Supabase client (`auth.get_user(access_token)`). Invalid/expired tokens return `401`.

**Alternative considered:** Local JWT verification with project secret. Rejected to avoid duplicating Supabase validation logic and key management.

**Note:** Validation uses backend infrastructure only; service role key remains server-side and is not exposed to Angular.

### 3. Derive `tipo_usuario` from profile tables, not a new DB column

After resolving `auth_user_id`, query `usuarios` and left-join logical role data:
- If row exists in `administradores` → `tipo_usuario = administrador`, include `id_administrador`.
- Else if row exists in `tecnicos` → `tipo_usuario = tecnico`, include `id_tecnico` and `estado_validacion`.
- Else if row exists in `clientes` → `tipo_usuario = cliente`, include `id_cliente`.
- Email comes from Supabase Auth user payload, not from `usuarios` (no email column in schema).

Priority order avoids ambiguity if seed data ever overlaps; current seed has one profile per user.

### 4. `GET /auth/me` response shape (Pydantic)

Return:
- `id_usuario`, `auth_user_id`, `nombres`, `apellidos`, `email`, `tipo_usuario`, `estado`
- Optional: `id_cliente`, `id_tecnico`, `id_administrador`, `estado_validacion`

Use explicit optional fields with `null` when not applicable.

### 5. Frontend session model: Supabase session + backend profile cache

`AuthService` stores Supabase session via SDK. After login, call `me()` with Bearer token and cache profile in a Signal (`currentUser` or `profile`). Guards and redirects use backend profile fields (`tipo_usuario`, `estado_validacion`).

**Alternative considered:** Infer role only from Supabase metadata. Rejected because business role lives in PostgreSQL profile tables.

### 6. Login UX on existing `/login` screen

Keep tabs and role selectors for visual continuity, but real login uses email/password only (Supabase determines account). Role tabs may pre-fill demo emails or show contextual titles; they must not block admin login if admin signs in without a visible admin tab (email-based routing after `me()`).

Registration tab remains non-functional or shows "Próximamente" unless trivial to stub; scope prioritizes login.

### 7. Route guards (functional, minimal)

Create guards such as:
- `authGuard` — requires Supabase session; else redirect `/login`.
- `clienteGuard`, `tecnicoValidadoGuard`, `adminGuard` — require matching `tipo_usuario` from cached `me()` profile; else redirect `/login` or a safe fallback.

`/panel-tecnico` requires `tipo_usuario === tecnico` **and** `estado_validacion === validado`.

Pending technician after login: stay on `/login` (or dedicated message state) with controlled message; do not enter `/panel-tecnico`.

### 8. Navbar session-aware links

When logged out: show `Iniciar sesión` and optionally `Registrarse` (both may route to `/login`).
When logged in: show display name (`nombres` + `apellidos`) and `Cerrar sesión`.
Do not add panel links to navbar (preserve existing layout spec intent).

### 9. HTTP Bearer attachment for `/auth/me` only in this change

Implement token forwarding inside `AuthService.me()` initially. Optional shared interceptor can be added if it stays scoped to authenticated FastAPI calls; do not retrofit all demo endpoints yet.

### 10. Preserve demo endpoints

No changes to `/clientes/demo/*`, `/tecnicos/demo/*`, `/admin/demo/*`, etc. They continue using hardcoded demo lookups until a follow-up auth migration change.

## Risks / Trade-offs

- **[Risk] Dual mode: real session + demo APIs** → Users may be logged in but panels still show demo data. **Mitigation:** Document as intentional staging step; acceptance criteria focus on auth routing, not full data scoping.
- **[Risk] Email not stored in `usuarios`** → Profile email depends on Supabase Auth response. **Mitigation:** Populate `email` in `/auth/me` from validated Auth user.
- **[Risk] Pending technician confusion** → User authenticates but cannot access technician panel. **Mitigation:** Explicit post-login message on `/login`.
- **[Risk] Public Supabase keys in frontend bundle** → Expected for anon key; RLS must protect data if direct DB access is ever added. **Mitigation:** Frontend uses Supabase only for Auth, not business queries.
- **[Risk] Guard race on refresh** → Session restore async before `me()` completes. **Mitigation:** Guard waits for auth initialization promise/signal before decision.

## Migration Plan

1. Implement backend `GET /auth/me` and verify with demo tokens via curl/Postman.
2. Add Supabase JS + AuthService; wire login/logout.
3. Add guards to protected routes.
4. Update navbar and login screen.
5. Run `npm run build` and manual acceptance with four demo accounts.
6. Rollback: revert auth router/guards; demo endpoints unaffected.

## Open Questions

- Exact demo passwords are managed in Supabase Auth dashboard, not repo; document in README/testing notes during implementation, not in committed secrets.
- Whether footer demo dashboard links should be hidden when auth is enabled (deferred; not required for acceptance).
