## Why

The technician panel already loads real available solicitudes from FastAPI, but submitting a cotización only updates local Angular Signals. Those quotes never reach Supabase, so `/detalle-solicitud/:id` and the client panel do not reflect new technician proposals. This change adds a real `POST /cotizaciones` endpoint and wires the panel form to persist quotes for the demo technician.

## What Changes

### Backend
- **New endpoint** `POST /cotizaciones` creating a row in the `cotizaciones` table for the demo technician
- **Request body** with `id_solicitud`, `precio`, `tiempo_estimado`, `descripcion_propuesta` (mapped to DB columns `monto`, `tiempo_estimado`, `descripcion`)
- **Validations:** solicitud exists, estado `pendiente`, category/zone match demo technician (reuse existing filter logic), no duplicate `(id_solicitud, id_tecnico)`
- **409 Conflict** when the demo technician already quoted the solicitud
- **422** for invalid/missing fields via Pydantic
- **New Pydantic schemas** `CotizacionRequest`, `CotizacionResponse`
- **New layer** `apis/cotizaciones.py`, `CotizacionesService`, `CotizacionesRepository` (or extend existing repositories)

### Frontend
- **`PanelTecnico`:** replace local `enviarCotizacion()` with `POST /cotizaciones` via service
- **Form states:** submitting, success, error (including 409 duplicate message)
- **On success:** update `ya_cotizada_por_tecnico`, increment `cotizaciones_count`, clear form; optionally append to sent-quotations UI from response
- **Keep** existing inline form (precio, tiempo, propuesta); Signals and `computed()` unchanged in pattern
- **No auth**, no direct Supabase from Angular

## Capabilities

### New Capabilities
- `cotizacion-api`: Backend `POST /cotizaciones` to create real cotizaciones for the demo technician with validation and duplicate handling

### Modified Capabilities
- `technician-dashboard`: Replace local-only cotización submit with backend POST; add submit loading/success/error states; update requirements that currently forbid backend HTTP on submit

## Impact

- **Backend:** New router `apis/cotizaciones.py`, schemas, service, repository methods; register router in `main.py`
- **Frontend:** New models and service method, updated `PanelTecnico` component/template
- **Downstream:** Created cotizaciones appear in `GET /solicitudes/{id}` and client panel cotización counts without further changes
- **No DB schema or seed changes**
- **No auth** — demo technician enforced server-side
- **Existing endpoints unchanged**
