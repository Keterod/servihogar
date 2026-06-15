## Context

El panel administrador existe como pantalla frontend con datos simulados, contadores derivados con Signals y acciones visuales para validar técnicos. El backend FastAPI ya está conectado a Supabase para flujos públicos, panel cliente, panel técnico, cotizaciones y valoraciones, pero todavía no existe autenticación real; por eso este cambio mantiene endpoints demo temporales bajo `/admin/demo`.

La base de datos actual ya contiene las entidades necesarias: `usuarios`, `clientes`, `tecnicos`, `solicitudes_servicio`, `cotizaciones`, `valoraciones`, `tecnico_categorias`, `categorias_servicio`, `tecnico_zonas` y `zonas`. No se requieren cambios en `database/schema.sql` ni `database/seed.sql`.

## Goals / Non-Goals

**Goals:**
- Backend: exponer `GET /admin/demo/resumen` con métricas reales del sistema.
- Backend: exponer `GET /admin/demo/tecnicos-pendientes` con técnicos cuyo `estado_validacion` sea `pendiente`.
- Backend: exponer acciones `PATCH` para aprobar o rechazar técnicos, validando existencia y estado actual.
- Frontend: conectar `/panel-administrador` a FastAPI, sin Supabase directo.
- Frontend: mostrar métricas reales, técnicos pendientes reales y estados de loading/error/empty/success.
- Frontend: actualizar lista y métricas tras aprobar o rechazar.
- Verificación: ejecutar build frontend.

**Non-Goals:**
- No implementar autenticación ni autorización real.
- No crear gestión completa de administradores, usuarios, categorías o reportes.
- No modificar `database/schema.sql`, `database/seed.sql`, `.env` ni `.env.example`.
- No cambiar rutas o contratos existentes de buscar técnicos, panel cliente, panel técnico, detalle de solicitud, cotizaciones o valoraciones.
- No introducir paginación, filtros avanzados ni búsqueda en técnicos pendientes.

## Decisions

1. **Nuevo dominio `admin` en backend**

   Crear `src/apis/admin.py`, `src/services/admin_service.py`, `src/repository/admin_repository.py` y `src/schemas/admin.py` mantiene el flujo obligatorio `main -> apis -> services -> repository` sin mezclar responsabilidades con repositorios de técnicos o solicitudes existentes.

   Alternativa considerada: ampliar APIs existentes (`tecnicos.py`, `solicitudes.py`, etc.). Se descarta porque el resumen cruza múltiples dominios y las acciones pertenecen a una vista administrativa demo.

2. **Endpoints demo explícitos bajo `/admin/demo`**

   El prefijo deja claro que no hay autenticación real y evita diseñar una seguridad incompleta. Cuando exista auth, estos endpoints podrán reemplazarse o protegerse sin cambiar la intención funcional.

   Alternativa considerada: usar `/admin` definitivo desde ahora. Se descarta para no ocultar la limitación actual de seguridad.

3. **Métricas calculadas en repository con consultas Supabase simples**

   `AdminRepository` debe contar entidades y estados con consultas directas a Supabase. Para el alcance actual, priorizar claridad y contratos estables por encima de una única consulta agregada compleja.

   Alternativa considerada: crear una vista o función SQL para el resumen. Se descarta porque el alcance prohíbe cambios de base de datos.

4. **Técnicos pendientes enriquecidos en backend**

   El backend debe devolver el técnico con datos del usuario, categorías y zonas para que Angular solo renderice datos ya preparados. `email` se modela como opcional porque el perfil interno `usuarios` no tiene columna `email`; si no está disponible mediante la integración backend actual, debe devolverse `null`.

   Alternativa considerada: que el frontend combine múltiples endpoints. Se descarta porque Angular no debe conocer detalles de Supabase ni ensamblar relaciones administrativas.

5. **Acciones idempotentes solo en lectura del estado actual, no en escritura silenciosa**

   Aprobar solo debe pasar de `pendiente` a `validado`, y rechazar solo de `pendiente` a `rechazado`. Si el técnico no existe o ya está en otro estado, el servicio debe responder un error controlado o un payload con el estado actual, según el patrón de errores existente.

   Alternativa considerada: devolver éxito aunque ya esté validado/rechazado. Se descarta porque ocultaría conflictos de estado en la UI administrativa.

6. **Frontend con servicio dedicado y Signals**

   Crear o adaptar un servicio Angular para los endpoints admin mantiene la comunicación HTTP fuera del componente. El componente debe guardar datos, loading, error, acción en curso y mensaje de éxito en Signals, con `computed()` para estados derivados.

   Alternativa considerada: hacer llamadas HTTP directamente en el componente. Se descarta por las reglas de arquitectura frontend del proyecto.

## Risks / Trade-offs

- **[Risk] Conteos inconsistentes durante varias consultas** -> Mitigation: aceptar consistencia eventual para el panel demo; refrescar el resumen después de cada acción.
- **[Risk] `email` no disponible en tablas públicas** -> Mitigation: devolver `email: null` y mostrar teléfono u otro dato disponible en la UI.
- **[Risk] Estado cambiado por otra operación antes de aprobar/rechazar** -> Mitigation: revalidar `estado_validacion` en el service/repository antes de actualizar y devolver error controlado o estado actual.
- **[Risk] Backend caído o Supabase no disponible** -> Mitigation: el frontend muestra error controlado y permite reintentar cargando datos otra vez.
- **[Risk] Regresión en rutas existentes** -> Mitigation: mantener cambios acotados a rutas admin y ejecutar `npm run build`.
