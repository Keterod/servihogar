## Why

The client request detail screen loads real cotizaciones from `GET /solicitudes/{id}`, but "Aceptar" and "Rechazar" only update local Angular Signals. Those decisions never reach Supabase, so reloads, the client dashboard, and the technician panel do not reflect accepted or rejected quotes. This change adds real PATCH endpoints and wires the detail screen to persist client decisions for the demo client.

## What Changes

### Backend
- **New endpoints** `PATCH /cotizaciones/{id_cotizacion}/aceptar` and `PATCH /cotizaciones/{id_cotizacion}/rechazar`
- **Accept flow:** validate cotización exists; validate solicitud belongs to demo client; set cotización `estado = aceptada`; reject other pending cotizaciones on the same solicitud; set solicitud `estado = en_proceso` (DB-valid state)
- **Reject flow:** validate cotización exists; validate solicitud belongs to demo client; set cotización `estado = rechazada`; leave solicitud unchanged when no cotización is accepted yet
- **Responses:** updated cotización (and solicitud estado when changed) via Pydantic schemas
- **Errors:** 404 (cotización/solicitud not found or not owned by demo client), 400 (invalid state transition), 409 (accept when another cotización is already accepted), 503 (persistence failure)
- **Extend** `CotizacionesService`, `CotizacionesRepository`, `apis/cotizaciones.py`; reuse demo client lookup from `SolicitudesRepository`

### Frontend
- **`DetalleSolicitud`:** replace local-only `aceptarCotizacion` / `rechazarCotizacion` with PATCH calls via service
- **Loading/error states** per action; update cotizaciones and solicitud estado from response or reload
- **Disable** accept/reject buttons when appropriate (already accepted/rejected, action in flight)
- **Keep** Signals, `computed()`, existing navigation and layout
- **No auth**, no direct Supabase from Angular

## Capabilities

### New Capabilities
<!-- None — endpoints extend existing cotizacion-api capability -->

### Modified Capabilities
- `cotizacion-api`: Add PATCH accept/reject endpoints with demo-client ownership validation and solicitud state transitions
- `client-request-detail`: Replace local-only accept/reject with backend PATCH; add loading/error feedback and persisted state

## Impact

- **Backend:** Extended `apis/cotizaciones.py`, `CotizacionesService`, `CotizacionesRepository`, `schemas/cotizacion.py`; possible helper in `SolicitudesRepository` to update solicitud estado
- **Frontend:** Extended `SolicitudService`, `DetalleSolicitud` component/template
- **Downstream:** `GET /solicitudes/{id}` and `GET /clientes/demo/solicitudes` reflect new states after reload without further API changes
- **No DB schema or seed changes**
- **No auth** — demo client enforced server-side
- **Existing endpoints unchanged** (`POST /cotizaciones`, GET detail, etc.)
