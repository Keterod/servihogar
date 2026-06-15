## Why

The `/panel-tecnico` screen still shows hardcoded mock solicitudes, cotizaciones, and servicios for Carlos Mendoza, while other flows (`/panel-cliente`, `/detalle-solicitud/:id`, `/solicitud-servicio`) already use real data from FastAPI and Supabase. Technicians cannot see which pending requests they can actually quote based on their categories and zones. This change connects the technician panel to the backend so the demo technician sees real available solicitudes without implementing authentication yet.

## What Changes

### Backend
- **New endpoint** `GET /tecnicos/demo/solicitudes-disponibles` returning pending solicitudes the demo technician (Carlos Mendoza, validated) can quote
- **Filtering** by demo technician categories, zones, and `estado = pendiente`; exclude finalizada, en_proceso, and cancelada
- **Response fields** per solicitud: `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cliente_nombre` (when available), `cotizaciones_count`, `ya_cotizada_por_tecnico`
- **New Pydantic schema** `SolicitudDisponibleResponse` (or equivalent) and repository/service methods with documented filter logic
- **Demo technician lookup** via fixed `auth_user_id` (same pattern as demo client), no auth middleware

### Frontend
- **Connect `/panel-tecnico`** to `GET /tecnicos/demo/solicitudes-disponibles` via service layer
- **Replace mock** `solicitudesDisponibles` with backend data; add loading, error, empty, and loaded states
- **Summary counts** derived with `computed()`: total disponibles, pendientes, cotizadas (when backend provides `ya_cotizada_por_tecnico`)
- **Actions per solicitud**: "Ver detalle" navigates to `/detalle-solicitud/:id`; "Enviar cotización" remains visual-only (no POST yet)
- **Keep mock** for cotizaciones enviadas and servicios aceptados until future backend endpoints exist
- **No direct Supabase** from Angular; no auth

## Capabilities

### New Capabilities
- `technician-available-requests-api`: Backend `GET /tecnicos/demo/solicitudes-disponibles` returning filtered pending solicitudes for the demo technician with category/zone matching and quotation metadata

### Modified Capabilities
- `technician-dashboard`: Replace hardcoded available solicitudes with backend-fetched data; add loading/error/empty states; add navigation to detail and visual-only cotización action; update summary computed values from real data

## Impact

- **Backend:** New schema in `src/schemas/solicitud.py` (or `tecnico.py`), new methods in `SolicitudesRepository`/`SolicitudesService` (or `TecnicosRepository`/`TecnicosService`), new route in `apis/tecnicos.py`
- **Frontend:** Extended `SolicitudService` (or `TecnicoService`), updated `PanelTecnico` component and template, new/extended models in `models/solicitud.ts`
- **No DB schema or seed changes**
- **No auth** — demo technician enforced server-side
- **Existing endpoints unchanged** (POST /solicitudes, GET /clientes/demo/solicitudes, GET /solicitudes/{id}, categorias, zonas, tecnicos)
- **Unchanged screens:** `/panel-cliente`, `/detalle-solicitud/:id`, `/solicitud-servicio`
