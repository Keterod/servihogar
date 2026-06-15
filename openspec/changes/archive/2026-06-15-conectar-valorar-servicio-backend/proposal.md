## Why

The `/valorar-servicio` screen only simulates submission locally. After a client accepts a cotización and the solicitud moves to `en_proceso`, there is no way to persist a real rating in Supabase. This change adds `POST /valoraciones` and wires the rating screen so the demo client can finalize and evaluate completed work through FastAPI.

## What Changes

### Backend
- **New endpoint** `POST /valoraciones` creating a row in `valoraciones`
- **Demo client** resolved server-side (no auth yet)
- **Request:** `id_solicitud`, `calificacion` (1–5), `comentario` (optional); optional sub-scores mapped to DB columns (`puntualidad`, `calidad`, `trato`, `precio`)
- **Resolve** `id_cotizacion` from the accepted cotización on the solicitud
- **Validate:** solicitud exists and belongs to demo client; accepted cotización exists; solicitud eligible (`en_proceso` or `finalizada`); calificación in range; no duplicate valoración for that cotización
- **On success:** set solicitud `estado = finalizada` when currently `en_proceso`
- **Response:** created valoración via Pydantic schema using real column names (`puntuacion`, `comentario`, `fecha_valoracion`, etc.)
- **Errors:** 404, 400, 409 (duplicate), 422, 503
- **Architecture:** `main → apis → services → repository`; register `apis/valoraciones.py` in `main.py`

### Frontend
- **Wire** `/valorar-servicio` to `POST /valoraciones` via service
- **Navigation** from `/detalle-solicitud/:id` with `?idSolicitud=` when solicitud is `en_proceso` or `finalizada`
- **Load context** (solicitud #, técnico aceptado, categoría) from existing `GET /solicitudes/{id}` or query param
- **Form:** calificación 1–5 (existing criteria UI), comentario, loading/success/error/duplicate states
- **On success:** confirmation message; optional navigation to panel cliente
- **Signals/computed** pattern preserved; no direct Supabase

## Capabilities

### New Capabilities
- `valoracion-api`: `POST /valoraciones` with demo-client validation, accepted-cotización resolution, duplicate prevention, and solicitud finalization

### Modified Capabilities
- `client-service-rating`: Replace simulated submission with real backend POST; load solicitud context from query param; add loading/error/duplicate UX
- `client-request-detail`: Navigate to `/valorar-servicio?idSolicitud=...` when solicitud is eligible; remove test-only navigation

## Impact

- **Backend:** New `apis/valoraciones.py`, `ValoracionesService`, `ValoracionesRepository`, `schemas/valoracion.py`; extend `SolicitudesRepository` for estado update and accepted-cotización lookup
- **Frontend:** New or extended rating service method; `ValorarServicio` component/template; `DetalleSolicitud` navigation update
- **Downstream:** `GET /solicitudes/{id}` and `GET /clientes/demo/solicitudes` reflect `finalizada` after rating; technician profile average may update via existing valoraciones queries
- **No DB schema or seed changes**
- **No auth** — demo client enforced server-side
- **Existing endpoints unchanged**
