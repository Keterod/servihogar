## 1. Backend — Schemas

- [x] 1.1 Create `src/schemas/admin.py` with Pydantic models for `AdminResumenResponse`, `TecnicoPendienteAdminResponse`, and technician validation action response
- [x] 1.2 Ensure pending technician schema includes `id_tecnico`, `nombres`, `apellidos`, optional `email`, optional `telefono`, `descripcion`, `experiencia_anios`, `fecha_registro`, `categorias`, and `zonas`

## 2. Backend — Repository

- [x] 2.1 Create `AdminRepository` in `src/repository/admin_repository.py` with count methods for users, clients, technicians, requests by state, technician validation states, quotations, and ratings
- [x] 2.2 Add repository method to fetch technicians with `estado_validacion = pendiente` joined with user profile data
- [x] 2.3 Add repository logic to attach category and zone display names for each pending technician
- [x] 2.4 Add repository method to fetch a technician by `id_tecnico` and current `estado_validacion`
- [x] 2.5 Add repository method to update `estado_validacion` to `validado` or `rechazado`

## 3. Backend — Service

- [x] 3.1 Create `AdminService` in `src/services/admin_service.py` to build the summary response from repository counts
- [x] 3.2 Add service method to return pending technicians mapped to Pydantic schemas with `email` as `None` when unavailable
- [x] 3.3 Add service method to approve a technician only when the technician exists and is currently `pendiente`
- [x] 3.4 Add service method to reject a technician only when the technician exists and is currently `pendiente`
- [x] 3.5 Return controlled not-found/conflict errors or current-state payloads for missing or already validated/rejected technicians

## 4. Backend — API Wiring

- [x] 4.1 Create `src/apis/admin.py` with `GET /admin/demo/resumen`
- [x] 4.2 Add `GET /admin/demo/tecnicos-pendientes`
- [x] 4.3 Add `PATCH /admin/demo/tecnicos/{id_tecnico}/aprobar`
- [x] 4.4 Add `PATCH /admin/demo/tecnicos/{id_tecnico}/rechazar`
- [x] 4.5 Register the admin router in `src/main.py` without removing existing routers

## 5. Frontend — Models and Service

- [x] 5.1 Add TypeScript interfaces for admin summary, pending technician, and validation action response
- [x] 5.2 Create or adapt an Angular admin service using the shared backend base URL from `src/app/env.ts`
- [x] 5.3 Add typed service methods for `GET /admin/demo/resumen`, `GET /admin/demo/tecnicos-pendientes`, `PATCH /admin/demo/tecnicos/{id}/aprobar`, and `PATCH /admin/demo/tecnicos/{id}/rechazar`
- [x] 5.4 Ensure the frontend does not import or call Supabase directly

## 6. Frontend — Panel Administrador

- [x] 6.1 Update `panel-administrador.ts` to load summary and pending technicians from the admin service on initialization
- [x] 6.2 Replace hardcoded summary/report data with backend-loaded metrics and computed display state
- [x] 6.3 Replace hardcoded technician validation data with the backend pending technician list
- [x] 6.4 Add Signals for summary, pending technicians, loading state, error state, action-in-progress state, and success message
- [x] 6.5 Add `computed()` values for empty/data/loading/error display decisions where useful
- [x] 6.6 Implement approve action with per-technician loading, backend call, list refresh, summary refresh, and success/error messages
- [x] 6.7 Implement reject action with per-technician loading, backend call, list refresh, summary refresh, and success/error messages
- [x] 6.8 Update `panel-administrador.html` to show metric cards, pending technician table/list, loading state, error state, empty state, and loaded state
- [x] 6.9 Remove or de-emphasize simulated category/user/report sections that are not backed by the new admin API

## 7. Verify

- [x] 7.1 Verify backend imports and FastAPI router registration do not break existing endpoints
- [x] 7.2 Run the frontend build with `npm run build` from `servihogar-frontend/`
- [x] 7.3 Spot-check routes `/buscar-tecnicos`, `/panel-cliente`, `/panel-tecnico`, and `/detalle-solicitud/:id` still compile/routable
