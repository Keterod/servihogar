## Context

The `/panel-cliente` component uses hardcoded mock data with three simulated requests. The backend has an existing `SolicitudesRepository` with `get_demo_cliente_id()` and `insert()` methods. A `GET /clientes/demo/solicitudes` endpoint can reuse the demo client lookup and query `solicitudes_servicio` joined with `categorias_servicio`, `zonas`, and `cotizaciones` for a complete response.

## Goals / Non-Goals

**Goals:**
- Backend: `GET /clientes/demo/solicitudes` endpoint returning solicitudes with category name, zone name, and cotización count
- Backend: New `SolicitudListResponse` Pydantic schema
- Frontend: Fetch real requests on `/panel-cliente` load
- Frontend: loading, error, empty states
- Frontend: "Ver detalle" navigates to `/detalle-solicitud/:id`
- Build passes

**Non-Goals:**
- No auth — demo client used
- No DB schema changes
- No changes to other screens
- No pagination or filtering on the list endpoint

## Decisions

1. **Reuse `SolicitudesRepository`** — Add a `get_by_cliente_id()` method to the existing repository rather than creating a new one. The demo client ID resolution is already implemented there.

2. **Query joins for display names** — The Supabase query joins `categorias_servicio` and `zonas` to return `nombre` fields alongside foreign keys. The cotización count uses a separate query or subquery.

3. **`SolicitudListResponse` schema** — Separate from `SolicitudResponse` because it includes display names (`categoria_nombre`, `zona_nombre`) and aggregated data (`cotizaciones_count`).

4. **Frontend model aligned to backend** — The local `Solicitud` interface is updated to match `SolicitudListResponse` fields: `id_solicitud`, `titulo`, `descripcion`, `direccion`, `estado`, `fecha_publicacion`, `categoria_nombre`, `zona_nombre`, `cotizaciones_count`.

5. **Route param for detail** — "Ver detalle" navigates to `/detalle-solicitud/{id_solicitud}` using `[routerLink]`. The existing `/detalle-solicitud` route will need the `:id` param, but that is out of scope for this change — only the navigation from the panel is updated.

## Risks / Trade-offs

- **[Low] Backend offline** → Component shows error message. Mitigation: `catchError` in service, error signal in component.
- **[Low] No requests yet** → Component shows empty state with suggestion to create one. Mitigation: condition on `solicitudes().length === 0`.
- **[Low] Cotización count may be zero** — Displayed as 0 in the table. This is correct for new requests.
