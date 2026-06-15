## Context

`/panel-tecnico` uses hardcoded Signals for `solicitudesDisponibles`, `cotizacionesEnviadas`, and `serviciosAceptados`. The client flow already creates real solicitudes via `POST /solicitudes` and lists them via `GET /clientes/demo/solicitudes`. The backend resolves demo users by fixed `auth_user_id` UUIDs in repository layers (client: `eb65fb3b-d00b-40b5-82e8-933cd3cd346c`; technician Carlos Mendoza: `9ce2ac73-1b61-40de-ac53-bafc12b3eb29`).

Carlos Mendoza is validated and serves Gasfitería menor and Electricidad básica in Huancayo Centro and El Tambo (seed data). Solicitudes must match both category and zone to appear as available. Seed includes one `pendiente` solicitud (Electricidad básica, El Tambo) already quoted by Carlos; one `finalizada` solicitud must not appear.

The panel template already has a table layout with summary cards, empty state branch, and local cotización form — only the data source for available solicitudes changes in v1.

## Goals / Non-Goals

**Goals:**
- Backend: `GET /tecnicos/demo/solicitudes-disponibles` with filtered pending solicitudes for demo technician
- Backend: Pydantic schema `SolicitudDisponibleResponse` with all required fields including `ya_cotizada_por_tecnico`
- Frontend: Fetch on `/panel-tecnico` load; loading, error, empty, loaded states
- Frontend: Summary `computed()` values from real available solicitudes
- Frontend: "Ver detalle" → `/detalle-solicitud/:id`; "Enviar cotización" as visual-only UI (existing inline form or button, no POST)
- Build passes; no Supabase in Angular

**Non-Goals:**
- No auth — demo technician enforced in service/repository
- No DB schema or seed changes
- No POST cotización endpoint
- No backend endpoints for cotizaciones enviadas or servicios aceptados (remain mock in panel for now)
- No changes to `/panel-cliente`, `/detalle-solicitud/:id`, `/solicitud-servicio`
- No fetching full technician profile from backend in this change (header can keep existing mock tecnico signal)

## Decisions

1. **Route on `apis/tecnicos.py`** — Add `GET /tecnicos/demo/solicitudes-disponibles` alongside existing tecnicos routes. Symmetric with `GET /clientes/demo/solicitudes` on solicitudes router. Demo prefix signals temporary auth bypass.

2. **Demo technician lookup in repository** — Add `get_demo_tecnico_id()` to `TecnicosRepository` (or extend `SolicitudesRepository`) querying `usuarios` → `tecnicos` by `auth_user_id = '9ce2ac73-1b61-40de-ac53-bafc12b3eb29'`. Mirror `get_demo_cliente_id()` pattern.

3. **Filter logic in repository, documented in service** — Two-step query approach for clarity:
   - Load demo technician's `id_categoria` list from `tecnico_categorias` and `id_zona` list from `tecnico_zonas`
   - Query `solicitudes_servicio` with `.eq("estado", "pendiente")`, `.in_("id_categoria", categorias)`, `.in_("id_zona", zonas)`, joins to `categorias_servicio`, `zonas`, and `clientes` → `usuarios` for `cliente_nombre`
   - Exclude solicitudes where estado is `finalizada`, `en_proceso`, or `cancelada` (only `pendiente` included)
   - Batch-fetch cotización counts and technician's own cotización ids for `ya_cotizada_por_tecnico`
   - Service method docstring explains matching rules

   **Alternative considered:** Single PostgREST filter with nested `tecnico_categorias` — rejected for readability and because solicitudes are not scoped to a single technician row.

4. **`SolicitudDisponibleResponse` schema** — Extends list-like fields with `cliente_nombre: str | None`, `cotizaciones_count: int`, `ya_cotizada_por_tecnico: bool`. Reuse field naming from `SolicitudListResponse` (`direccion_referencia` → `direccion`).

5. **Include already-quoted pendiente solicitudes** — Return solicitudes the technician already quoted (`ya_cotizada_por_tecnico = true`) so the panel can show them with a "cotizada" indicator and exclude from "pendientes de cotizar" count. Do not hide them entirely unless product requires — user asked for `ya_cotizada_por_tecnico` flag.

6. **Service placement** — Add `obtener_solicitudes_disponibles()` to `SolicitudesService` (solicitud-centric query) or `TecnicosService`. Prefer `SolicitudesService` + `SolicitudesRepository` methods to keep solicitud queries together; route handler lives in `tecnicos.py` and delegates to solicitudes service.

7. **Frontend service method** — Add `solicitudesDisponiblesTecnico()` to `SolicitudService` calling `GET /tecnicos/demo/solicitudes-disponibles`. Return `null` on HTTP error (same pattern as `solicitudesCliente()`).

8. **PanelTecnico loading pattern** — Mirror `PanelCliente`: `cargando`, `error`, `solicitudesDisponibles` signals; fetch in `ngOnInit` with `takeUntilDestroyed`; optional router reload on NavigationEnd to `/panel-tecnico`.

9. **Computed summary** — `totalDisponibles = solicitudesDisponibles().length`; `pendientesDeCotizar = filter(!ya_cotizada_por_tecnico)`; `cotizadas = filter(ya_cotizada_por_tecnico)`. Keep mock computed counts for cotizaciones enviadas and servicios aceptados until future API.

10. **"Enviar cotización" stays local** — Button opens/selects inline form; submit still updates local Signals only. No HTTP on submit. Documented non-goal.

11. **RouterLink for detail** — Add `RouterLink` import; "Ver detalle" links to `/detalle-solicitud/{{ id_solicitud }}`.

## Risks / Trade-offs

- **[Low] Supabase `.in_()` with empty category/zone lists** → Return empty array if technician has no categories/zones configured. Mitigation: seed ensures Carlos has both.
- **[Low] New solicitudes from POST in non-matching zone/category** → Not shown to Carlos. Mitigation: expected behavior; demo creates matching data via form.
- **[Medium] technician-dashboard spec conflicts with mock-only requirements** → Delta spec MODIFIED requirements replace hardcoded id 2/3 and gasfitería-only filter with backend-driven behavior.
- **[Low] Cotizaciones enviadas still mock** → Panel may show mock sent quotation for solicitud #1 while available list comes from backend. Mitigation: non-goal for v1; future endpoint will align.
- **[Low] Backend offline** → Error state in component. Mitigation: `catchError(() => of(null))`.

## Migration Plan

1. Deploy backend endpoint first (backward compatible).
2. Update frontend service and `PanelTecnico`.
3. Verify with seed: only pendiente + matching category/zone solicitudes appear; finalizada excluded; El Tambo electricidad shows with `ya_cotizada_por_tecnico = true`.
4. Run `npm run build`.
5. Rollback: revert frontend to mock; backend endpoint unused but harmless.

## Open Questions

- None blocking — technician header profile can remain mock until a dedicated demo profile endpoint is requested.
