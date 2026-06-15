## Why

ServiHogar ya consume datos reales vía FastAPI y Supabase, pero la autenticación sigue siendo visual: el login no crea sesión, los paneles por rol no están protegidos y el backend resuelve usuarios demo con `auth_user_id` fijos. Con usuarios demo ya creados en Supabase Auth, es el momento de conectar login real, identificar roles y redirigir por tipo de usuario sin romper los endpoints demo existentes.

## What Changes

### Backend
- **New endpoint** `GET /auth/me` that accepts `Authorization: Bearer <supabase_jwt>`.
- **JWT validation** against Supabase Auth and lookup of the internal profile in `usuarios` by `auth_user_id`.
- **Profile response** with user identity, derived `tipo_usuario`, role-specific IDs, and `estado_validacion` for technicians.
- **Controlled errors:** `401` for missing/invalid token, `404` when Auth user exists but has no row in `usuarios`.
- **Architecture preserved:** `main -> apis -> services -> repository` with Pydantic schemas.
- **Demo endpoints unchanged** for now; no mandatory auth migration across existing business APIs.

### Frontend
- **Supabase Auth client** in Angular using only public URL and anon/publishable key (no service role).
- **AuthService** with `login`, `logout`, `getSession`, `getCurrentUser`, and `me()` calling `GET /auth/me`.
- **Real login** on `/login` with controlled error messages and session persistence via Supabase Auth.
- **Role-based redirect** after login: cliente → `/panel-cliente`, técnico validado → `/panel-tecnico`, técnico pendiente → blocked message, administrador → `/panel-administrador`.
- **Route guards** for protected panels; unauthenticated users redirect to `/login`.
- **Navbar session UI:** login/register links when logged out; user name and logout when logged in.
- **Business data unchanged:** Angular continues calling FastAPI for business endpoints; Supabase JS is used only for Auth in this change.
- **Registration deferred:** keep registration tab visual or disabled; focus on real login first.

## Capabilities

### New Capabilities
- `auth-me-api`: Backend authenticated current-user endpoint that validates Supabase JWT and returns the linked ServiHogar profile with role metadata.
- `frontend-auth`: Frontend Supabase Auth integration, AuthService, session handling, role-based redirects, route guards, and navbar session actions.

### Modified Capabilities
- `frontend-public-screens`: Replace visual-only login behavior with real Supabase Auth login, controlled errors, and post-login routing by role.
- `frontend-layout`: Update navbar requirements to reflect authenticated vs unauthenticated session states without exposing role dashboards in public navigation.

## Impact

- **Backend:** New auth router, service, repository, schemas, and dependency-injected auth header parsing; existing demo lookups remain until a later migration.
- **Frontend:** New Supabase JS dependency, auth config file, AuthService, guards, updates to `login-register`, `navbar`, and route configuration; optional HTTP interceptor for Bearer token on `/auth/me`.
- **Security:** No service role in frontend; no `.env`, `schema.sql`, or `seed.sql` changes in this change.
- **Dependencies:** Add `@supabase/supabase-js` to `servihogar-frontend`.
- **Regression scope:** Public routes (`/inicio`, `/buscar-tecnicos`, `/perfil-tecnico/:id`) and existing demo-backed business flows must keep working without mandatory login except for protected panels.
