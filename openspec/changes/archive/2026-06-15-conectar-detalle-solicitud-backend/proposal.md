## Why

The `/detalle-solicitud/:id` screen still displays hardcoded mock data for solicitud #1 and three simulated cotizaciones, even though `/panel-cliente` already navigates with the real `id_solicitud` and the backend stores real solicitudes and cotizaciones in Supabase. Users who click "Ver detalle" on any request see incorrect information. This change connects the request detail screen to FastAPI so it reflects the selected solicitud and its real cotizaciones.

## What Changes

### Backend
- **New endpoint** `GET /solicitudes/{id_solicitud}` returning full detail for a demo-client solicitud
- **Response includes** solicitud fields (titulo, descripcion, direccion, estado, fecha_publicacion, categoria_nombre, zona_nombre) and nested cotizaciones with technician info
- **404** when the solicitud does not exist or does not belong to the demo client
- **Empty cotizaciones array** when none exist
- **New Pydantic schemas** `SolicitudDetalleResponse`, `CotizacionDetalleResponse`
- **Repository/service methods** reusing demo client lookup from existing `SolicitudesRepository`

### Frontend
- **DetalleSolicitud rewrite:** fetch from `GET /solicitudes/{id}` using route param `:id`
- **Replace mock** solicitud and cotizaciones with backend data
- **States added:** loading, error, notFound, loaded
- **Empty cotizaciones state:** "Aún no hay cotizaciones para esta solicitud."
- **Accept/reject actions** remain local UI-only (no backend mutation yet)
- **No auth**, no direct Supabase from Angular

## Capabilities

### New Capabilities
- `request-detail-api`: Backend `GET /solicitudes/{id_solicitud}` endpoint returning solicitud detail with cotizaciones for the demo client

### Modified Capabilities
- `client-request-detail`: Replace simulated solicitud and cotizaciones with backend-fetched data; add loading/error/notFound/empty-cotizaciones states; route uses `/detalle-solicitud/:id`

## Impact

- **Backend:** New schemas in `src/schemas/solicitud.py`, new methods in `SolicitudesRepository`/`SolicitudesService`, new route in `apis/solicitudes.py`
- **Frontend:** Updated models, `SolicitudService.obtenerDetalle(id)`, full rewrite of `DetalleSolicitud` component and template
- **No DB schema or seed changes**
- **No auth** — demo client ownership enforced server-side
- **Existing endpoints unchanged** (POST /solicitudes, GET /clientes/demo/solicitudes, categorias, zonas, tecnicos)
