## Context

ServiHogar tiene layout base, pantallas públicas y flujo cliente (`panel-cliente`, `detalle-solicitud`) con Signals. El panel técnico es placeholder. En `detalle-solicitud`, Carlos Mendoza ya cotizó la solicitud “Fuga de agua en cocina” (Gasfitería menor, Huancayo Centro).

Este sprint implementa el flujo del técnico en un solo componente, con datos simulados locales y coherencia narrativa con el cliente (sin servicio compartido).

## Goals / Non-Goals

**Goals:**

- Un solo `panel-tecnico` con secciones apiladas y scroll vertical.
- Tarjetas para solicitudes, cotizaciones enviadas y servicios aceptados (patrón `panel-cliente`).
- Solicitudes disponibles solo de **Gasfitería menor**; ids 1, 2, 3 del universo cliente.
- Una cotización por solicitud; al enviar, mover de disponibles a enviadas.
- Formulario: precio (S/), tiempo estimado, propuesta.
- Signals y computed según estructura acordada.
- Carlos Mendoza: Huancayo Centro, `validado`, puede cotizar.

**Non-Goals:**

- Subcomponentes, pestañas, backend, services, models, rutas, auth, flujo administrador.
- Mostrar electricidad u otras categorías como disponibles para Carlos.
- Sincronizar cotizaciones con `panel-cliente` en runtime.
- Cambiar estados de validación interactivamente en la demo.

## Decisions

### 1. Un solo componente, secciones apiladas

**Decisión:** Todo en `panel-tecnico` con scroll vertical. Secciones: header → resumen (contadores) → solicitudes disponibles → detalle + formulario → cotizaciones enviadas → servicios aceptados.

**Rationale:** Mismo patrón que `panel-cliente`; sin complejidad extra.

### 2. Técnico simulado

| Campo | Valor |
|-------|-------|
| Nombre | Carlos Mendoza |
| Especialidad | Gasfitería menor / Fontanería general |
| Zona | Huancayo Centro |
| Calificación | 4.8 |
| Validación | `validado` (demo) |

### 3. Universo de solicitudes (ids 1, 2, 3)

| ID | Categoría | Descripción | Zona | En panel técnico |
|----|-----------|-------------|------|------------------|
| 1 | Gasfitería menor | Fuga de agua en cocina | Huancayo Centro | **No disponible** — Carlos ya cotizó → cotización enviada (pendiente) |
| 2 | Gasfitería menor | Cambio de llave de paso | El Tambo | **Disponible** para cotizar |
| 3 | Gasfitería menor | Reparación de desagüe en baño | Chilca | **Disponible** para cotizar |

Cada solicitud incluye: id, categoría, descripción breve, zona, fecha tentativa, dirección aproximada.

**Nota:** En `panel-cliente`, ids 2 y 3 muestran otras categorías del historial del cliente demo. En el panel técnico representan **otras solicitudes del mercado** con esos ids en el mock académico (sin estado compartido).

### 4. Solicitud id 1 — ya cotizada

**Decisión:** No aparece en `solicitudesDisponibles`. Precargada en `cotizacionesEnviadas` con estado `pendiente`, datos alineados con `detalle-solicitud` (precio 85, 2 horas, propuesta de Carlos).

**Servicio aceptado inicial (opcional):** puede existir un servicio aceptado previo simulado; la solicitud id 1 permanece como cotización pendiente hasta que el cliente acepte en su flujo.

### 5. Presentación: tarjetas

**Decisión:** Solicitudes disponibles, cotizaciones enviadas y servicios aceptados usan **tarjetas** como `panel-cliente`. Solicitud seleccionada con borde/estilo activo.

### 6. Formulario de cotización

**Signal:** `formCotizacion = signal({ precio: '', tiempo: '', propuesta: '' })`

| Campo | Tipo | Validación |
|-------|------|------------|
| Precio estimado | number, mostrado S/ | > 0 |
| Tiempo estimado | text (ej. "2 horas") | no vacío |
| Propuesta | textarea | no vacío |

Al cambiar `solicitudSeleccionada` sin enviar → reset de `formCotizacion`.

### 7. Una cotización por solicitud

**Decisión:** `enviarCotizacion()`:
1. Valida formulario y `estadoValidacion === 'validado'`.
2. Agrega a `cotizacionesEnviadas` con estado `pendiente` y fecha simulada.
3. Remueve solicitud de `solicitudesDisponibles`.
4. Limpia formulario y `solicitudSeleccionada`.

No re-cotización en la misma sesión.

### 8. Cotizaciones enviadas (tarjetas)

Campos: solicitud asociada (id), categoría, descripción breve, precio, tiempo estimado, propuesta, estado (`pendiente` | `aceptada` | `rechazada`), fecha simulada de envío.

Precarga: cotización de Carlos para solicitud id 1 (pendiente).

### 9. Servicios aceptados (tarjetas)

Campos: categoría, descripción, zona, cliente simulado, estado (`en_proceso` | `finalizado`), fecha.

Precarga: al menos un servicio simulado (puede vincularse narrativamente a trabajo previo de Carlos).

### 10. Estado de validación

**Decisión:** Badge visual para `pendiente`, `validado`, `rechazado`. Demo: `validado`.

Si `pendiente` o `rechazado`: botón enviar cotización **deshabilitado** (no aplica en demo). No hay UI para cambiar el estado.

### 11. Arquitectura Signals

```typescript
tecnico = signal({ ... })
solicitudesDisponibles = signal([...])      // ids 2, 3
cotizacionesEnviadas = signal([...])        // incluye id 1
serviciosAceptados = signal([...])
solicitudSeleccionada = signal<Solicitud | null>(null)
formCotizacion = signal({ precio: '', tiempo: '', propuesta: '' })
estadoValidacion = signal<'pendiente' | 'validado' | 'rechazado'>('validado')
```

**Computed:**
- `totalSolicitudesDisponibles`
- `totalCotizacionesEnviadas`
- `totalServiciosAceptados`
- `puedeEnviarCotizacion` — formulario válido, solicitud seleccionada, técnico validado

### 12. Filtro por especialidad

**Decisión:** Solo solicitudes **Gasfitería menor** en disponibles. No electricidad ni pintura para Carlos.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| ids 2–3 difieren en categoría entre panel cliente y técnico | Documentado: mocks independientes, misma numeración narrativa |
| Cotización técnico no actualiza panel cliente | Aceptado; sin backend ni estado global |
| Solicitud id 1 en detalle vs panel técnico | Mismos datos de cotización Carlos en precarga |
| Pantalla larga en móvil | Scroll vertical; tarjetas apiladas |

## Migration Plan

1. `npm run build`
2. `/panel-tecnico` — verificar secciones, tarjetas, cotizar id 2 o 3
3. Confirmar id 1 no en disponibles, sí en enviadas
4. Confirmar Signals/computed en código
5. Responsive ~375px

## Open Questions

- _(cerradas — decisiones del usuario incorporadas)_
