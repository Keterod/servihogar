## Context

The `/solicitud-servicio` form uses hardcoded categories and zones, no service layer, and only simulates submission. The `/perfil-tecnico/:id` "Solicitar cotización" button goes to `/login`. The backend has no endpoint for creating service requests. The `solicitudes_servicio` table exists in Supabase with a demo client record.

## Goals / Non-Goals

**Goals:**
- Backend: `POST /solicitudes` endpoint with Pydantic validation, demo client hardcoded lookup
- Frontend: `SolicitudService` with `crearSolicitud(data)` calling `POST /solicitudes`
- Frontend: Category/zone dropdowns populated from backend API
- Frontend: Technician reference via query params (`tecnicoId`, `tecnicoNombre`, `categoriaId`)
- Frontend: Form validation, loading, success, and error states
- Frontend: "Solicitar cotización" button navigates to `/solicitud-servicio` with query params
- Build passes

**Non-Goals:**
- No real auth — uses demo client lookup
- No image upload — dropzone stays as visual placeholder
- No `id_tecnico` in DB insertion (column doesn't exist in table)
- No changes to other screens
- No DB schema or seed modifications

## Decisions

1. **Demo client lookup by auth_user_id** — Since there's no login, the backend uses a hardcoded `auth_user_id` matching the seed client (`eb65fb3b-d00b-40b5-82e8-933cd3cd346c`). The service resolves `id_cliente` from the `clientes` + `usuarios` tables. When real auth is implemented, this will be replaced with the authenticated user's ID.

2. **`id_tecnico` accepted but not stored** — The frontend can send `id_tecnico` as context. The backend receives it in the Pydantic schema but does not insert it into `solicitudes_servicio` (no column exists). It could be used for future reference.

3. **Query params for technician reference** — The `PerfilTecnico` component generates a URL with `tecnicoId`, `tecnicoNombre`, and optionally `categoriaId` query params. The `SolicitudServicio` component reads these via `ActivatedRoute.queryParams` and shows a technician reference card.

4. **Signal-based form state** — Existing pattern preserved: `signal()` for each field, `computed()` for `puedeEnviar`. Added signals for `loading`, `success`, `error`, `categorias`, `zonas`, `tecnicoNombre`.

5. **`SolicitudRequest` schema mirrors form fields** — The Pydantic schema accepts `id_categoria`, `id_zona`, `titulo`, `descripcion`, `direccion_referencia`. `titulo` is derived from the selected category name and a brief description prefix.

## Risks / Trade-offs

- **[Medium] Demo client hardcoded** — Once real auth is added, the lookup must change. Mitigation: the lookup is isolated to the service layer, making replacement straightforward.
- **[Low] Backend offline** → Form shows error banner. Mitigation: `catchError` in service, error signal in component.
- **[Low] No `id_tecnico` in DB** → The request is not directly associated with a specific technician. Mitigation: Client selects category; technicians in that category see the request. Future schema migration could add the column.
