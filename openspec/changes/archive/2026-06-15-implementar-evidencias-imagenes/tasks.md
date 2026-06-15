## 1. Supabase Storage (manual / documentación)

- [ ] 1.1 Crear bucket `servihogar-evidencias` en Supabase Dashboard
- [ ] 1.2 Configurar políticas RLS: INSERT autenticado en `solicitudes/{id}/*` solo dueño cliente; INSERT en `tecnicos/{id}/portafolio/*` solo técnico dueño; SELECT según decisión de bucket público read
- [x] 1.3 Verificar que no se usa service role en frontend

## 2. Backend — schemas y repositorios

- [x] 2.1 Añadir schemas Pydantic: `ImagenSolicitudRequest/Response`, extender `SolicitudDetalleResponse` con `imagenes[]`, `PortafolioCreateRequest/Response`
- [x] 2.2 Crear `ImagenesSolicitudRepository` (insert, count_by_solicitud, list_by_solicitud)
- [x] 2.3 Extender `TecnicosRepository` con `insert_portafolio`, `count_portafolio_visible`, `list_portafolio_for_tecnico` (panel, incluye ocultos)

## 3. Backend — servicios y APIs solicitud

- [x] 3.1 Implementar `SolicitudesService.registrar_imagen(id_solicitud, id_cliente, data)` con validación path y límite 5
- [x] 3.2 Extender `obtener_detalle_por_id` / `_build_detalle_response` para incluir `imagenes`
- [x] 3.3 Añadir rutas en `apis/solicitudes.py`: `POST /solicitudes/{id}/imagenes`, `GET /solicitudes/{id}/imagenes` con `require_cliente` o acceso compartido de detalle
- [x] 3.4 Validar MIME/extensión y prefijo de path en servicio

## 4. Backend — servicios y APIs portafolio

- [x] 4.1 Implementar `TecnicosService.agregar_portafolio(id_tecnico, data)` y `listar_mi_portafolio(id_tecnico)`
- [x] 4.2 Añadir rutas en `apis/tecnicos.py`: `GET /tecnicos/me/portafolio`, `POST /tecnicos/me/portafolio` con `require_tecnico_validado`
- [x] 4.3 Confirmar `GET /tecnicos/{id}` sigue filtrando `estado=visible`

## 5. Frontend — servicio Storage

- [x] 5.1 Crear `StorageService` (o extender Supabase client): upload con validación MIME/tamaño, sanitizar nombre, paths según design
- [x] 5.2 Helper para URL pública o path completo según configuración del bucket

## 6. Frontend — solicitud cliente

- [x] 6.1 Extender modelos TypeScript con `ImagenSolicitud`
- [x] 6.2 Añadir selector de imágenes + previews en `solicitud-servicio` (Signals)
- [x] 6.3 Tras `POST /solicitudes` exitoso: subir imágenes y llamar `POST /solicitudes/{id}/imagenes` con Bearer
- [x] 6.4 Manejar errores parciales (solicitud creada pero fallo en imagen)

## 7. Frontend — detalle solicitud

- [x] 7.1 Extender `SolicitudDetalle` con `imagenes[]`
- [x] 7.2 Galería en `detalle-solicitud.html` (cliente y técnico autorizado)

## 8. Frontend — panel y perfil técnico

- [x] 8.1 Métodos en servicio: `obtenerMiPortafolio()`, `crearPortafolioItem()` con Bearer
- [x] 8.2 Sección portafolio en `panel-tecnico` (listar + formulario agregar)
- [x] 8.3 Verificar `perfil-tecnico` renderiza `imagen_url` de Storage correctamente

## 9. Verificación

- [ ] 9.1 Cliente crea solicitud con 2 fotos → aparecen en detalle
- [ ] 9.2 Cliente A no ve/registra imágenes de cliente B
- [ ] 9.3 Técnico autorizado ve galería en detalle; no autorizado → 403
- [ ] 9.4 Técnico sube portafolio → visible en `/perfil-tecnico/:id`
- [ ] 9.5 Rechazar archivo >5 MB o PDF en UI
- [x] 9.6 `npm run build` OK
- [x] 9.7 Smoke test backend endpoints nuevos con TestClient (401/403/201)
