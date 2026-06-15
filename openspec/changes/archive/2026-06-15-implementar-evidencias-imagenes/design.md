## Context

ServiHogar ya autentica clientes, técnicos y administradores vía Supabase Auth + FastAPI. Las tablas `imagenes_solicitud` y `portafolio_tecnico` existen en `schema.sql` con columnas `imagen_url`. El README de `database/` documenta Storage pero los buckets aún no están cableados en la app.

Flujos autenticados actuales usan endpoints `/me/...` y Bearer token. El frontend ya tiene cliente Supabase (`@supabase/supabase-js`) para Auth con anon key.

## Goals / Non-Goals

**Goals:**

- Permitir al cliente adjuntar imágenes al crear una solicitud y verlas en el detalle.
- Permitir al técnico validado subir evidencias de trabajos a su portafolio.
- Mostrar portafolio en perfil público del técnico.
- Guardar binarios en Supabase Storage; metadata en PostgreSQL vía backend.
- Validar tipo MIME y tamaño (5 MB máx.) en frontend y backend.
- Respetar permisos: dueño de solicitud, técnico autorizado o admin para ver imágenes de solicitud; técnico solo su portafolio.

**Non-Goals:**

- `documentos_tecnico`, validación documental, registro con adjuntos.
- Edición avanzada de imágenes (recorte, filtros).
- CDN custom o buckets separados por entorno en código.
- Migración de URLs placeholder del seed a Storage real (opcional manual).

## Decisions

### 1. Upload híbrido: Storage en frontend, metadata en backend

**Decisión:** El frontend sube archivos directamente a Supabase Storage con anon key + políticas RLS. Tras upload exitoso, llama al backend para persistir metadata (`imagen_url` = path o public URL acordada).

**Alternativa descartada:** Multipart al backend → backend sube con service role. Aumenta carga en API y tamaño de requests.

**Alternativa descartada:** Metadata insertada desde Angular vía Supabase client a Postgres. Viola regla de no consumir Supabase directo para datos de negocio.

### 2. Bucket único `servihogar-evidencias`

**Decisión:** Un bucket con prefijos:

- `solicitudes/{id_solicitud}/{timestamp}-{nombreSanitizado}`
- `tecnicos/{id_tecnico}/portafolio/{timestamp}-{nombreSanitizado}`

**Alternativa:** Buckets separados (`solicitudes`, `portafolio-tecnicos` del README). Rechazada para simplificar políticas iniciales; se documenta en Supabase.

### 3. Flujo de imágenes en solicitud (dos fases)

1. `POST /solicitudes` (autenticado, existente) crea solicitud → `id_solicitud`.
2. Frontend sube cada archivo a Storage bajo `solicitudes/{id}/...`.
3. `POST /solicitudes/{id_solicitud}/imagenes` registra `{ imagen_url, descripcion? }` por imagen (o batch en un solo body).

**Por qué:** Reutiliza creación actual; evita transacciones multipart complejas; permite reintentar uploads fallidos.

### 4. Portafolio técnico

- `GET /tecnicos/me/portafolio` — lista ítems del técnico autenticado (incluye ocultos para panel).
- `POST /tecnicos/me/portafolio` — registra metadata tras upload a Storage.
- `GET /tecnicos/{id}` — sigue exponiendo solo `estado=visible` (comportamiento actual del repositorio).

Sin DELETE en v1 salvo necesidad; `estado=oculto` puede ser fase 2.

### 5. Acceso a imágenes de solicitud

Reutilizar `verificar_acceso_detalle` para endpoints de imágenes y extender `SolicitudDetalleResponse` con:

```json
"imagenes": [{ "id_imagen", "imagen_url", "descripcion", "fecha_subida" }]
```

Visibilidad de URLs: bucket **público** para lectura de evidencias de solicitud y portafolio visible, **o** signed URLs generadas por backend. **Recomendación v1:** bucket público read-only para paths bajo `solicitudes/` y `tecnicos/*/portafolio/` con upload restringido por RLS autenticado — más simple para MVP.

### 6. Validación de archivos

| Capa | Regla |
|------|--------|
| Frontend | `accept="image/jpeg,image/png,image/webp"`, chequeo `file.size <= 5*1024*1024`, magic bytes opcional |
| Backend | Validar extensión/MIME declarado, path prefix, solicitud/portafolio ownership |
| Storage RLS | Solo usuarios autenticados escriben en paths permitidos |

### 7. Cambios de schema

**No se requieren cambios a `schema.sql`** para v1: tablas existentes son suficientes.

**Configuración Supabase (manual, fuera de repo):**

- Crear bucket `servihogar-evidencias`.
- Políticas Storage: INSERT autenticado en paths propios; SELECT público o autenticado según decisión §5.

Documentar pasos en `database/README.md` solo si el usuario lo pide; este change no modifica ese archivo por restricción de alcance.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Orphan files en Storage si falla POST metadata | Frontend borra objeto Storage si backend rechaza; log en backend |
| Bucket público expone URLs adivinables | Paths incluyen id + timestamp; no listado de bucket; evaluar signed URLs en v2 |
| Límite de imágenes no enforced en DB | Validar máx. 5 por solicitud en backend |
| Políticas Storage mal configuradas | Checklist de prueba manual post-deploy |
| Specs desactualizados en technician-dashboard (demo endpoints) | Deltas corrigen a `/tecnicos/me/...` donde aplique en este change |

## Migration Plan

1. Crear bucket y políticas en Supabase Dashboard.
2. Desplegar backend con nuevos endpoints.
3. Desplegar frontend con upload UI.
4. Seed existente sigue con URLs placeholder hasta reemplazo manual opcional.
5. Rollback: desactivar UI; endpoints nuevos son aditivos.

## Open Questions

- ¿Bucket público read vs signed URLs para producción? (MVP: público read recomendado.)
- ¿Permitir eliminar imágenes de solicitud antes de cotizaciones? (Fuera de v1; solo add.)
- ¿Máximo de ítems de portafolio por técnico? (Proponer 20 en backend.)
