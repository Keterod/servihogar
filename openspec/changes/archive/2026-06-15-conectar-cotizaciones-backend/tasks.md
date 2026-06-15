## 1. Backend — Schemas

- [x] 1.1 Add `CotizacionRequest` Pydantic model: `id_solicitud`, `precio` (> 0), `tiempo_estimado`, `descripcion_propuesta` (non-empty)
- [x] 1.2 Add `CotizacionResponse` Pydantic model: `id_cotizacion`, `id_solicitud`, `id_tecnico`, `precio`, `tiempo_estimado`, `descripcion_propuesta`, `estado`, `fecha_creacion`

## 2. Backend — Repository

- [x] 2.1 Create `CotizacionesRepository` with `exists_for_tecnico(id_solicitud, id_tecnico)` and `insert(data)` targeting `cotizaciones` table
- [x] 2.2 Add `get_solicitud_for_cotizacion(id_solicitud)` returning id, estado, id_categoria, id_zona (or reuse/extend `SolicitudesRepository`)

## 3. Backend — Service & API

- [x] 3.1 Create `CotizacionesService.crear_cotizacion_demo(data)` validating demo technician, solicitud pendiente, category/zone eligibility, duplicate → None with distinct error codes
- [x] 3.2 Create `apis/cotizaciones.py` with `POST /cotizaciones` returning 201, 400, 404, 409, 422
- [x] 3.3 Register cotizaciones router in `main.py`

## 4. Frontend — Model & Service

- [x] 4.1 Add `CotizacionRequest` and `CotizacionResponse` interfaces to models
- [x] 4.2 Add `crearCotizacion(data)` to service calling `POST /cotizaciones`; return response on 201, `'duplicate'` on 409, `null` on other errors

## 5. Frontend — PanelTecnico Component

- [x] 5.1 Add `enviandoCotizacion`, `errorCotizacion`, `exitoCotizacion` signals; wire `enviarCotizacion()` to service POST
- [x] 5.2 On 201: update `ya_cotizada_por_tecnico` and `cotizaciones_count`, reset form/selection, show success
- [x] 5.3 On 409: show duplicate message and mark solicitud as already quoted
- [x] 5.4 On error: show generic failure message; disable submit while loading
- [x] 5.5 Update template with loading/success/error feedback for cotización submit

## 6. Verify

- [x] 6.1 Test `POST /cotizaciones` success, 409 duplicate (solicitud #2), 400 non-pending, 404 invalid id
- [x] 6.2 Verify new cotización appears in `GET /solicitudes/{id}` and `/detalle-solicitud/:id`
- [x] 6.3 Verify panel marks solicitud as cotizada after success; duplicate attempt shows 409 message
- [x] 6.4 Run `npm run build` in `servihogar-frontend/`
