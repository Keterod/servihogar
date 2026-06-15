## Why

Las solicitudes del cliente y el portafolio del técnico ya tienen tablas de metadata (`imagenes_solicitud`, `portafolio_tecnico`) y el diseño de BD prevé Supabase Storage, pero la aplicación no permite subir ni mostrar imágenes reales. Sin evidencias visuales, clientes no pueden contextualizar averías y técnicos no pueden demostrar trabajos previos en su perfil público.

## What Changes

### Imágenes de solicitud (cliente)

- **Adjuntar fotos** al crear solicitud en `/solicitud-servicio` (opcional, múltiples).
- **Subida a Supabase Storage** bucket `servihogar-evidencias` en ruta `solicitudes/{id_solicitud}/{timestamp-nombreArchivo}`.
- **Registro de metadata** en `imagenes_solicitud` vía backend autenticado (no insert directo desde Angular a Postgres).
- **Visualización** en `/detalle-solicitud/:id` para cliente dueño, técnico autorizado y administrador.
- **Validaciones:** `image/jpeg`, `image/png`, `image/webp`; máximo 5 MB por imagen; límite razonable por solicitud (p. ej. 5 imágenes).

### Portafolio / evidencias del técnico

- **Subida autenticada** desde `/panel-tecnico` por técnico validado.
- **Storage** en `servihogar-evidencias/tecnicos/{id_tecnico}/portafolio/{timestamp-nombreArchivo}`.
- **Metadata** en `portafolio_tecnico` (`titulo`, `descripcion`, `imagen_url`, `estado=visible`).
- **Perfil público** `/perfil-tecnico/:id` muestra portafolio desde backend (ya parcialmente implementado).
- **Gestión básica** en panel técnico: listar y agregar ítems (sin flujo de documentos de validación).

### Backend

- Nuevos endpoints autenticados para registrar/listar imágenes de solicitud y portafolio.
- Extender `GET /solicitudes/{id}` con array `imagenes`.
- Reutilizar lógica de acceso ya existente (`require_cliente`, `require_tecnico_validado`, `require_administrador`, `verificar_acceso_detalle`).
- Service role **solo en backend** para operaciones de metadata; frontend usa anon key únicamente para Storage/Auth.

### Frontend

- Servicio de subida a Storage (anon key) + servicios HTTP para metadata.
- UI mínima en formulario de solicitud, detalle, panel técnico y perfil público.

### Explícitamente fuera de alcance

- Documentos de validación del técnico (`documentos_tecnico`).
- Carga de documentos en registro.
- Botón o pantalla de documentos en admin.
- Cambios al flujo de aprobación/rechazo de técnicos.

## Capabilities

### New Capabilities

- `solicitud-imagenes-api`: Endpoints backend para registrar y listar imágenes de solicitud; inclusión en detalle autenticado.
- `portafolio-tecnico-api`: Endpoints backend para que el técnico autenticado gestione metadata de portafolio.
- `frontend-image-upload`: Subida a Supabase Storage desde Angular, validación MIME/tamaño, integración con flujos cliente y técnico.

### Modified Capabilities

- `client-service-request`: Formulario con selector de imágenes y flujo post-creación de solicitud.
- `client-request-detail`: Galería de imágenes de la solicitud en detalle.
- `service-request-api`: POST autenticado y endpoints de imágenes asociados (delta sobre creación).
- `request-detail-api`: Respuesta de detalle incluye `imagenes`; acceso autenticado por rol.
- `perfil-tecnico-backend`: Portafolio alimentado por uploads reales (URLs de Storage).
- `technician-dashboard`: Sección de portafolio para ver y agregar evidencias.

## Impact

- **Supabase:** Bucket `servihogar-evidencias` y políticas RLS de Storage (configuración en panel Supabase; **no** cambios a `schema.sql` salvo confirmación futura).
- **Backend:** Nuevos routers/repositorios/servicios/schemas; extensión de `SolicitudesService` y detalle.
- **Frontend:** Nuevo servicio Storage, cambios en `solicitud-servicio`, `detalle-solicitud`, `panel-tecnico`, `perfil-tecnico`; posible extensión de modelos TypeScript.
- **Seguridad:** Sin service role en Angular; validación de MIME/tamaño en frontend y backend; paths de Storage acotados por rol.
- **Sin tocar:** `.env`, `documentos_tecnico`, registro de técnicos, panel admin de validación.
