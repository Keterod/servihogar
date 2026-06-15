## Why

The `/solicitud-servicio` screen and its "Solicitar cotización" button on `/perfil-tecnico/:id` still use hardcoded mock data. The backend now connects to Supabase but has no endpoint to create service requests. This change closes the last gap in the public user flow: browsing technicians → viewing a profile → requesting a service — all with real data.

## What Changes

### Backend
- **New endpoint** `POST /solicitudes` that inserts into `solicitudes_servicio` using a demo client ID (no auth yet)
- **Pydantic schema** for request validation (id_categoria, titulo, descripcion, direccion, id_zona, id_tecnico optional)
- **Demo client lookup** — resolves the seed client by auth_user_id until real auth exists

### Frontend
- **Navigation change:** "Solicitar cotización" button on `/perfil-tecnico/:id` now goes to `/solicitud-servicio?tecnicoId=X&tecnicoNombre=Y` instead of `/login`
- **SolicitudServicio rewrite:** reads query params for technician reference, fetches categorias/zonas from backend, posts to `POST /solicitudes`, adds loading/error/success states
- **New service:** `SolicitudService` with `crearSolicitud(data)` method
- **Form validation preserved** via existing Signals + computed
- **No image upload** — the dropzone stays as visual placeholder

## Capabilities

### New Capabilities
- `service-request-api`: Backend `POST /solicitudes` endpoint and frontend service for creating service requests in Supabase via FastAPI

### Modified Capabilities
- `client-service-request`: Replace simulated submission with real `POST /solicitudes`; replace hardcoded categorias/zonas with backend-fetched options; add technician reference via query params; add loading/error/success states
- `frontend-public-screens`: Change "Solicitar cotización" navigation on `/perfil-tecnico/:id` from `/login` to `/solicitud-servicio` with query params

## Impact

- **Backend:** New schema `SolicitudRequest`/`SolicitudResponse`, new router in `src/apis/solicitudes.py`, new service/repo in `src/services/` and `src/repository/`, register router in `main.py`
- **Frontend:** `SolicitudService`, full `SolicitudServicio` component rewrite, navigation update in `PerfilTecnico` template
- **No DB schema changes** — uses existing `solicitudes_servicio` table
- **No auth** — demo client used until login is implemented
