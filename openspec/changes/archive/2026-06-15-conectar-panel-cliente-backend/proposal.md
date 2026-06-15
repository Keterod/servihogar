## Why

The `/panel-cliente` screen shows three hardcoded mock requests. The backend now has `POST /solicitudes` creating real data in Supabase, but the client dashboard never fetches it. Users who create requests from `/solicitud-servicio` cannot see them in the panel. This change connects the client dashboard to the backend.

## What Changes

### Backend
- **New endpoint** `GET /clientes/demo/solicitudes` returning all requests for the demo client with category name, zone name, and cotización count

### Frontend
- **PanelCliente rewrite:** fetches from `GET /clientes/demo/solicitudes`, replaces hardcoded mock data
- **Service addition:** new method in existing or new service to fetch client requests
- **Model update:** `Solicitud` interface aligned with backend response (id_solicitud, titulo, descripcion, direccion, estado, categoria, zona, fecha_publicacion, cotizaciones)
- **States added:** loading, error empty
- **Navigation:** "Ver detalle" navigates to `/detalle-solicitud/:id` instead of static route
- **No auth** — demo client used

## Capabilities

### New Capabilities
- `client-dashboard-api`: Backend `GET /clientes/demo/solicitudes` endpoint returning demo client service requests with category, zone, and cotización count

### Modified Capabilities
- `client-dashboard`: Replace simulated requests with backend-fetched data; add loading/error/empty states; change "Ver detalle" navigation to pass `id_solicitud`

## Impact

- **Backend:** New `SolicitudListResponse` schema, new endpoint in `apis/solicitudes.py`, new repository method for querying by cliente_id with joins to categorias_servicio, zonas, and cotizaciones count
- **Frontend:** Updated `Solicitud` model, new or updated service method, full `PanelCliente` component rewrite
- **No DB schema changes**
- **No auth** — demo client lookup via hardcoded auth_user_id
