## Context

`/panel-tecnico` fetches available solicitudes via `GET /tecnicos/demo/solicitudes-disponibles` and shows an inline cotización form (precio, tiempo, propuesta). `enviarCotizacion()` currently pushes to a local `cotizacionesEnviadas` signal and sets `ya_cotizada_por_tecnico` in memory only. `/detalle-solicitud/:id` already loads real cotizaciones via `GET /solicitudes/{id}` from the `cotizaciones` table.

The DB schema defines:
- `cotizaciones`: `id_solicitud`, `id_tecnico`, `monto`, `descripcion`, `tiempo_estimado`, `estado` (default `pendiente`), `fecha_envio`
- Unique constraint `uq_cotizacion_solicitud_tecnico` on `(id_solicitud, id_tecnico)`
- Check `monto > 0`

Demo technician lookup and category/zone filtering already exist in `TecnicosRepository` and `SolicitudesRepository.get_disponibles_for_tecnico()`.

## Goals / Non-Goals

**Goals:**
- Backend: `POST /cotizaciones` persisting a cotización for demo technician Carlos Mendoza
- Backend: validate solicitud exists, pendiente, matches technician categories/zones; reject duplicates with 409
- Frontend: submit form via HTTP; loading, success, error (409) states
- Frontend: on success update available solicitud flags (`ya_cotizada_por_tecnico`, `cotizaciones_count`)
- Created cotización visible in `/detalle-solicitud/:id` without changes to that screen
- Build passes

**Non-Goals:**
- No auth middleware
- No DB schema or seed changes
- No GET endpoint for technician's sent cotizaciones (mock `cotizacionesEnviadas` section may stay or append from POST response only)
- No accept/reject cotización mutations
- No changes to `/panel-cliente`, `/detalle-solicitud`, `/solicitud-servicio` except shared models/service if needed

## Decisions

1. **New router `apis/cotizaciones.py`** — Single `POST /cotizaciones` route. Symmetric with `POST /solicitudes`. Register in `main.py` alongside existing routers.

2. **Dedicated `CotizacionesService` + `CotizacionesRepository`** — Keeps insert/duplicate logic separate from read-heavy `SolicitudesRepository`. Reuse `TecnicosRepository.get_demo_tecnico_id()` and category/zone helpers for eligibility checks.

3. **Eligibility reuse** — Before insert, load solicitud by id with `id_categoria` and `id_zona`; verify `estado = pendiente` and that category/zone are in demo technician's lists (same rules as available solicitudes). Return 404 if solicitud not found, 400 if not pendiente or not eligible.

4. **Duplicate detection** — Query existing cotización by `(id_solicitud, id_tecnico)` before insert; return HTTP 409 with clear message. Also catch Supabase unique violation as fallback.

5. **Schema field mapping** — API request uses friendly names aligned with frontend:
   - `precio` → DB `monto`
   - `descripcion_propuesta` → DB `descripcion`
   - `tiempo_estimado` → DB `tiempo_estimado`
   Response `CotizacionResponse`: `id_cotizacion`, `id_solicitud`, `id_tecnico`, `precio`, `tiempo_estimado`, `descripcion_propuesta`, `estado`, `fecha_creacion` (from `fecha_envio`)

6. **Pydantic validation** — `precio > 0`, non-empty `descripcion_propuesta`, `id_solicitud` required; `tiempo_estimado` optional but frontend requires non-empty (client-side + optional server min length).

7. **Frontend service** — Add `crearCotizacion()` to `SolicitudService` or new `CotizacionService` (prefer extend `SolicitudService` for cohesion with solicitud flows). Handle 409 distinctly for user message; other errors → generic error state.

8. **Panel submit flow** — Add `enviandoCotizacion` and `errorCotizacion` signals. On success: update `solicitudesDisponibles` item (`ya_cotizada_por_tecnico: true`, `cotizaciones_count + 1`), optionally push to `cotizacionesEnviadas` from response, clear selection and form, show brief success feedback.

9. **Remove contradictory local-only behavior** — Delete `nextCotizacionId` fake id generation for new submissions; keep mock seed entry in `cotizacionesEnviadas` or replace with response-driven append only for session.

## Risks / Trade-offs

- **[Low] Mock sent-quotations section out of sync** → Only new quotes from this session appear from POST response; pre-loaded mock for solicitud #1 remains until a future list endpoint. Mitigation: documented non-goal.
- **[Low] Race double-submit** → User clicks twice quickly. Mitigation: disable submit button while `enviandoCotizacion`; second request returns 409.
- **[Low] Category/zone mismatch edge case** → Solicitud created before technician profile change. Mitigation: server-side eligibility check mirrors GET available list.
- **[Low] Supabase insert failure** → 503 via existing exception handler. Mitigation: generic error message in UI.

## Migration Plan

1. Deploy backend `POST /cotizaciones` first.
2. Update frontend service and `PanelTecnico`.
3. Verify: quote from panel → appears in `/detalle-solicitud/:id`; duplicate → 409 message.
4. Rollback: revert frontend to local submit; endpoint unused but harmless.

## Open Questions

- None blocking — `tiempo_estimado` required on frontend, optional in DB (varchar nullable); server accepts empty string as null or rejects empty — prefer reject empty to match UI validation.
