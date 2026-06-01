## Context

ServiHogar tiene layout, pantallas públicas, flujo cliente y flujo técnico (`technician-dashboard`). Carlos Mendoza aparece como técnico `validado` en `/panel-tecnico`. El panel administrador es placeholder. Este sprint cierra el triángulo de roles con mocks locales y Signals.

## Goals / Non-Goals

**Goals:**

- Un solo `panel-administrador`, secciones apiladas, scroll vertical.
- Grid de 6 contadores en resumen; solicitudes/cotizaciones solo en reportes.
- Lista única de técnicos con badge; validar/rechazar solo `pendiente`; mensaje de confirmación.
- Categorías con nomenclatura flujo cliente; agregar con anti-duplicados.
- 5 usuarios simulados con rol y estado.
- Reportes con métricas fijas + computed donde aplique.

**Non-Goals:**

- Subcomponentes, pestañas, backend, services, models, rutas, auth, reversión de estados.
- Sincronizar validación con otros paneles.
- Email/calificación en técnicos; editar/eliminar categorías.

## Decisions

### 1. Layout: un componente, secciones apiladas

1. Header — Panel administrador
2. Resumen general — grid 6 contadores
3. Técnicos — lista única con badges y acciones
4. Categorías — listado + formulario
5. Usuarios registrados — tarjetas
6. Reportes básicos — tarjetas métricas

### 2. Resumen general (grid 6 contadores, computed)

- Total técnicos
- Técnicos pendientes
- Técnicos validados
- Técnicos rechazados
- Categorías
- Usuarios registrados

Solicitudes y cotizaciones **no** van aquí; solo en reportes.

### 3. Técnicos — lista única

Campos por técnico: id, nombre, especialidad, zona, estado (`pendiente`|`validado`|`rechazado`), fechaRegistro.

| Nombre | Especialidad | Zona | Estado inicial |
|--------|--------------|------|----------------|
| Carlos Mendoza | Gasfitería menor | Huancayo Centro | validado |
| Luis Arango | Electricidad básica | El Tambo | pendiente |
| Rosa Huamán | Gasfitería menor | Chilca | pendiente |
| Pedro Vargas | Pintura básica | Huancayo Centro | rechazado |

**Notas de coherencia:**
- Carlos Mendoza `validado` — coherente con `panel-tecnico`.
- **No usar Roberto Salas** (cotiza en `detalle-solicitud`; evitar contradicción).
- **Rosa Huamán** en lugar de Ana Ruiz (evitar conflicto con búsqueda pública).

Solo `pendiente`: botones Validar / Rechazar. Sin reversión en `validado`/`rechazado`.

**Acciones:** `validarTecnico(id)` / `rechazarTecnico(id)` con `tecnicos.update()`; `mensajeAccion.set('Técnico validado correctamente')` o rechazo equivalente.

### 4. Categorías iniciales (nomenclatura flujo cliente)

- Gasfitería menor
- Electricidad básica
- Mantenimiento de computadoras
- Pintura básica
- Armado de muebles

No usar "Fontanería". Agregar categoría: nombre obligatorio, descripción opcional. Evitar duplicados por nombre (mensaje simple, no agregar).

### 5. Usuarios simulados (5)

| Nombre | Rol | Estado sugerido |
|--------|-----|-----------------|
| Mariana Quispe | cliente | activo |
| Carlos Mendoza | tecnico | activo |
| Luis Arango | tecnico | pendiente |
| Rosa Huamán | tecnico | pendiente |
| Administrador Demo | administrador | activo |

Mostrar: nombre, rol, estado (activo/pendiente/rechazado). Email opcional mínimo o omitir si no requerido — user didn't specify email for users, only role and estado.

### 6. Reportes básicos

Tarjetas con métricas:

| Métrica | Fuente |
|---------|--------|
| Solicitudes publicadas | Valor fijo narrativo (ej. 12) |
| Cotizaciones registradas | Valor fijo narrativo (ej. 28) |
| Servicios finalizados | Valor fijo narrativo (ej. 7) |
| Técnicos activos | computed → técnicos validados |
| Usuarios registrados | computed → totalUsuarios |

Signal `reportes` para valores fijos; computed para técnicos activos y usuarios.

### 7. Arquitectura Signals

```typescript
tecnicos = signal<TecnicoAdmin[]>([...])
categorias = signal<Categoria[]>([...])
usuarios = signal<Usuario[]>([...])
reportes = signal({ solicitudesPublicadas: 12, cotizacionesRegistradas: 28, serviciosFinalizados: 7 })
formCategoria = signal({ nombre: '', descripcion: '' })
mensajeAccion = signal('')
```

**Computed:**
- `totalTecnicos`, `tecnicosPendientes`, `tecnicosValidados`, `tecnicosRechazados`
- `totalCategorias`, `totalUsuarios`, `tecnicosActivos`
- `puedeAgregarCategoria` — nombre no vacío y no duplicado

### 8. Presentación visual

Tarjetas y badges como `panel-cliente` / `panel-tecnico`. Badges validación: pendiente (amarillo), validado (verde), rechazado (rojo).

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Mocks no sincronizados entre paneles | Documentado; coherencia narrativa por nombres |
| Rosa Huamán vs Ana Ruiz en búsqueda | Nombre distinto en admin |
| Pantalla larga | Scroll vertical |
| Categorías admin vs home público | Admin usa nomenclatura cliente |

## Migration Plan

1. `npm run build`
2. `/panel-administrador` — validar/rechazar, agregar categoría, verificar mensajes
3. Signals/computed presentes
4. Responsive ~375px

## Open Questions

- _(cerradas — decisiones del usuario incorporadas)_
