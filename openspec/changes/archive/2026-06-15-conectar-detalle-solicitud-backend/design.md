## Context

`/panel-cliente` fetches real solicitudes via `GET /clientes/demo/solicitudes` and navigates to `/detalle-solicitud/:id`. The detail component reads `:id` from the route for the header but still renders mock solicitud #1 and three hardcoded cotizaciones. The backend already has `SolicitudesRepository` with demo client lookup, list query with joins, and access to `cotizaciones`, `tecnicos`, and `usuarios` tables via Supabase.

Seed data includes solicitud #1 with cotizaciones and solicitud #2 with one cotización; newer solicitudes from `POST /solicitudes` may have zero cotizaciones.

## Goals / Non-Goals

**Goals:**
- Backend: `GET /solicitudes/{id_solicitud}` returning solicitud detail + cotizaciones for demo client only
- Backend: Pydantic schemas `SolicitudDetalleResponse`, `CotizacionDetalleResponse`
- Frontend: Fetch detail on route param change; display real fields and cotizaciones
- Frontend: loading, error, notFound, empty cotizaciones states
- Frontend: Keep accept/reject as local signal updates (no POST/PATCH yet)
- Build passes

**Non-Goals:**
- No auth — demo client enforced in service/repository
- No DB schema or seed changes
- No endpoints to accept/reject cotizaciones
- No changes to panel-cliente, solicitud-servicio, or other screens except shared service/models
- No technician rating fetch unless trivially available from existing joins

## Decisions

1. **Extend `apis/solicitudes.py`** — Add `GET /solicitudes/{id_solicitud}` alongside existing POST and list routes. Same router, same service class.

2. **Ownership check in service** — Resolve demo `id_cliente`, fetch solicitud by id, return `None` if missing or `id_cliente` mismatch → API returns 404. Avoids exposing other clients' solicitudes by id guessing.

3. **`SolicitudDetalleResponse` schema** — Extends list fields with `cotizaciones: list[CotizacionDetalleResponse]`. Map DB columns: `direccion_referencia` → `direccion`, `fecha_publicacion` → response field, `monto` → `precio`, `descripcion` (cotización) → `descripcion_propuesta`, `fecha_envio` → `fecha_creacion`.

4. **Cotización query with technician join** — Query `cotizaciones` filtered by `id_solicitud`, join `tecnicos` → `usuarios` for `tecnico_nombre` (nombres + apellidos), use `tecnicos.descripcion` as `tecnico_descripcion`. Return empty list if none.

5. **Frontend service method** — Add `obtenerDetalle(id: number)` to existing `SolicitudService` calling `GET /solicitudes/{id}`. Return `null` on 404, propagate other errors for error state.

6. **Route param subscription** — `DetalleSolicitud` reads `:id` from `ActivatedRoute` and refetches when id changes (snapshot on init; optional paramMap subscribe if navigating between details without destroy).

7. **Accept/reject stays local** — Map backend cotización `estado` to UI; accept/reject buttons update signals only until a future change adds mutation endpoints. Do not inject fake cotizaciones when backend returns `[]`.

8. **Timeline/paso logic** — Derive from real `solicitud.estado` and cotizaciones count/estados via `computed()` instead of hardcoded mock state.

## Risks / Trade-offs

- **[Low] Solicitud without cotizaciones** → Empty state message. Mitigation: `@if (cotizaciones().length === 0)` branch in template.
- **[Low] Accept/reject not persisted** → User action resets on reload. Mitigation: documented non-goal; UI remains for prototype continuity.
- **[Low] Technician rating not in cotizaciones table** → Omit `calificacion` or compute optionally from valoraciones; mock UI field can show "—" if unavailable.
- **[Low] Backend offline** → Error state in component. Mitigation: `catchError` distinguishes 404 vs other errors.

## Migration Plan

1. Deploy backend endpoint first (backward compatible).
2. Update frontend service and detail component.
3. Verify with seed solicitud #1 (has cotizaciones) and a new solicitud from POST (empty cotizaciones).
4. Rollback: revert frontend to mock; backend endpoint unused but harmless.

## Open Questions

- None blocking — technician rating in cotización cards is optional; show only if backend provides it or omit from v1 response.
