## 1. Backend — Schemas

- [x] 1.1 Create `src/schemas/auth.py` with Pydantic models for `AuthMeResponse` including optional role-specific fields
- [x] 1.2 Define `tipo_usuario` as a constrained string/enum (`cliente`, `tecnico`, `administrador`)
- [x] 1.3 Ensure response supports nullable `id_cliente`, `id_tecnico`, `id_administrador`, and `estado_validacion`

## 2. Backend — Repository

- [x] 2.1 Create `AuthRepository` in `src/repository/auth_repository.py`
- [x] 2.2 Add method to validate Supabase JWT via `auth.get_user(access_token)` and return Auth user payload
- [x] 2.3 Add method to fetch `usuarios` row by `auth_user_id`
- [x] 2.4 Add method to resolve linked `clientes`, `tecnicos`, and `administradores` records for profile assembly
- [x] 2.5 Map repository results to role metadata without modifying schema or seed files

## 3. Backend — Service

- [x] 3.1 Create `AuthService` in `src/services/auth_service.py`
- [x] 3.2 Add method to extract Bearer token from `Authorization` header and reject missing/invalid tokens with controlled errors
- [x] 3.3 Add method to build `AuthMeResponse` with email from Supabase Auth and profile fields from PostgreSQL
- [x] 3.4 Derive `tipo_usuario` from linked profile tables with administrator precedence over technician and client
- [x] 3.5 Return not-found when Auth user exists but no `usuarios` row is linked

## 4. Backend — API Wiring

- [x] 4.1 Create `src/apis/auth.py` with `GET /auth/me`
- [x] 4.2 Return HTTP 401 for missing, invalid, or expired tokens
- [x] 4.3 Return HTTP 404 when token is valid but profile is missing in `usuarios`
- [x] 4.4 Register auth router in `src/main.py` without removing existing routers
- [x] 4.5 Verify existing demo endpoints still respond without auth headers

## 5. Frontend — Dependencies and Configuration

- [x] 5.1 Add `@supabase/supabase-js` to `servihogar-frontend/package.json` and install dependencies
- [x] 5.2 Create secure frontend Supabase config module (e.g. `src/app/supabase.env.ts`) with URL and anon/publishable key only
- [x] 5.3 Ensure no service role key is referenced anywhere in frontend code

## 6. Frontend — Models and AuthService

- [x] 6.1 Add TypeScript interfaces for auth profile / `me()` response aligned with backend schema
- [x] 6.2 Create `AuthService` using Supabase JS client singleton
- [x] 6.3 Implement `login(email, password)` with Supabase Auth and follow-up `me()` call
- [x] 6.4 Implement `logout()`, `getSession()`, and `getCurrentUser()` using Signals where appropriate
- [x] 6.5 Implement `me()` calling `GET /auth/me` with Bearer token from current session
- [x] 6.6 Add auth initialization on app startup to restore session and profile when possible

## 7. Frontend — Login Screen

- [x] 7.1 Wire `login-register.ts` sign-in submission to `AuthService.login()`
- [x] 7.2 Add Signals for loading, error, and pending-technician message states
- [x] 7.3 Implement role-based redirect after successful login (`cliente`, validated `tecnico`, `administrador`)
- [x] 7.4 Block pending technicians from `/panel-tecnico` and show controlled pending-account message
- [x] 7.5 Keep registration tab visual or mark as deferred without breaking login flow
- [x] 7.6 Update `login-register.html` for error, loading, and pending-account UI states

## 8. Frontend — Guards and Routes

- [x] 8.1 Create auth and role guards (`authGuard`, `clienteGuard`, `tecnicoValidadoGuard`, `adminGuard`)
- [x] 8.2 Protect `/panel-cliente`, `/panel-tecnico`, and `/panel-administrador` in `app.routes.ts`
- [x] 8.3 Redirect unauthenticated users to `/login`
- [x] 8.4 Ensure guards wait for auth initialization before deciding access

## 9. Frontend — Navbar

- [x] 9.1 Update `navbar.ts` to consume `AuthService` session/profile Signals
- [x] 9.2 Show `Iniciar sesión` / `Registrarse` when logged out
- [x] 9.3 Show user display name and `Cerrar sesión` when logged in
- [x] 9.4 Implement logout navigation back to `/login`
- [x] 9.5 Keep role dashboard links out of navbar

## 10. Verify

- [x] 10.1 Verify login with `cliente.demo@servihogar.com` routes to `/panel-cliente`
- [x] 10.2 Verify login with `tecnico.demo@servihogar.com` routes to `/panel-tecnico`
- [x] 10.3 Verify login with `admin.demo@servihogar.com` routes to `/panel-administrador`
- [x] 10.4 Verify login with `tecnico.pendiente@servihogar.com` shows pending message and does not enter validated technician panel
- [x] 10.5 Verify logout clears session and returns to `/login`
- [x] 10.6 Verify protected routes redirect to `/login` without session
- [x] 10.7 Run `npm run build` from `servihogar-frontend/`
- [x] 10.8 Spot-check public routes `/inicio`, `/buscar-tecnicos`, and `/perfil-tecnico/:id` remain accessible without login
