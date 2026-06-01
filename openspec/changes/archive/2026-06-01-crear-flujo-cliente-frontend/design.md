## Context

El frontend de ServiHogar está construido con Angular 21, TypeScript, CSS y componentes standalone. Ya existe el layout base con navbar, footer y navegación pública funcionando. Las pantallas públicas (inicio, búsqueda de técnicos, perfil de técnico, login) están implementadas con datos simulados usando propiedades plain y getters.

Los componentes del flujo cliente ya existen como shells vacíos:
- `src/app/components/solicitud-servicio/`
- `src/app/components/panel-cliente/`
- `src/app/components/detalle-solicitud/`
- `src/app/components/valorar-servicio/`

Las rutas ya están definidas en `app.routes.ts` sin parámetros.

El flujo real del cliente implica: publicar solicitud → recibir cotizaciones → aceptar cotización → recibir servicio → valorar servicio.

## Goals / Non-Goals

**Goals:**
- Implementar contenido visual en las 4 pantallas del cliente existentes
- Usar Angular Signals para estado local solo en estos componentes
- Mantener datos simulados coherentes entre pantallas
- Validar visualmente el flujo completo antes de integrar backend
- Mantener estructura simple y código académico

**Non-Goals:**
- Conectar con el backend API
- Implementar autenticación real
- Agregar librerías externas
- Modificar el backend existente
- Implementar flujo de técnico o administrador
- Usar formularios reactivos complejos
- Crear servicios de estado globales
- Migrar pantallas públicas a Signals
- Reubicar componentes existentes
- Agregar parámetros de ruta (:id)
- Modificar el botón "Solicitar servicio" del perfil técnico

## Decisions

### 1. Estructura de componentes

**Decisión:** Usar los componentes existentes en sus ubicaciones actuales. No crear carpeta `client/`.

**Rationale:** Los componentes ya existen como shells vacíos. Reubicar sería trabajo innecesario para un caso académico.

**Estructura final:**
```
src/app/components/
├── solicitud-servicio/   ← implementar
├── panel-cliente/        ← implementar
├── detalle-solicitud/    ← implementar
├── valorar-servicio/     ← implementar
├── buscar-tecnicos/      ← sin cambios
├── perfil-tecnico/       ← sin cambios
└── ...
```

### 2. Manejo de estado con Signals

**Decisión:** Usar `signal()` para estado reactivo local y `computed()` para valores derivados, SOLO en los 4 componentes del flujo cliente.

**Rationale:** Angular Signals es la forma moderna de manejar estado reactivo en Angular 21. Los componentes existentes de pantallas públicas mantienen su patrón actual (propiedades plain + getters).

**Alternativas consideradas:**
- Migrar todos los componentes: Innecesario para este sprint
- Servicios inyectables: Más complejo para datos estáticos de demostración

### 3. Rutas

**Decisión:** Mantener rutas actuales sin parámetros.

**Rationale:** Los datos son simulados internamente. No se necesita identificar solicitudes específicas por URL.

**Rutas actuales (sin cambios):**
```typescript
{ path: 'solicitud-servicio', component: SolicitudServicio },
{ path: 'panel-cliente', component: PanelCliente },
{ path: 'detalle-solicitud', component: DetalleSolicitud },
{ path: 'valorar-servicio', component: ValorarServicio },
```

### 4. Datos simulados

**Decisión:** Datos coherentes entre pantallas, duplicados en cada componente por simplicidad académica.

**Rationale:** No se crea servicio compartido. Cada componente define sus datos internos, pero mantienen coherencia visual.

**Datos base:**
- Solicitud: Gasfitería menor, Huancayo Centro, "Fuga de agua en cocina"
- Técnicos: Carlos Mendoza, Luis Arango, Roberto Salas
- Estados: pendiente, en_proceso, finalizado, cancelado

### 5. Formulario de solicitud

**Decisión:** Formulario con 6 campos usando controles HTML estándar.

**Campos:**
| Campo | Tipo | Control |
|-------|------|---------|
| Categoría | text | `<select>` |
| Zona | text | `<select>` |
| Descripción | text | `<textarea>` |
| Fecha tentativa | date | `<input type="date">` |
| Horario preferido | text | `<select>` o texto |
| Dirección aproximada | text | `<input type="text">` |

**Categorías simuladas:** Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, Armado de muebles

**Zonas simuladas:** Huancayo Centro, El Tambo, Chilca, San Carlos

### 6. Panel del cliente

**Decisión:** Mostrar 3 solicitudes simuladas con información resumida.

**Información por solicitud:**
- Categoría
- Descripción breve
- Zona
- Fecha tentativa
- Estado (pendiente, en_proceso, finalizado, cancelado)
- Número de cotizaciones
- Botón "Ver detalle"

### 7. Detalle de solicitud

**Decisión:** Mostrar 1 solicitud simulada con 3 cotizaciones de diferentes técnicos.

**Cotizaciones:**
| Técnico | Especialidad | Calificación |
|---------|--------------|--------------|
| Carlos Mendoza | Fontanería general | 4.8 |
| Luis Arango | Reparaciones menores | 4.5 |
| Roberto Salas | Gasfitería residencial | 4.2 |

**Estados de cotización:** pendiente, aceptada, rechazada

**Flujo de aceptación:**
1. Usuario hace clic en "Aceptar" de una cotización
2. La cotización seleccionada cambia a "aceptada"
3. Las demás cambian a "rechazada" o se deshabilitan
4. Se muestra mensaje de confirmación
5. La solicitud se presenta como "en_proceso"

**Flujo de rechazo:**
1. Usuario hace clic en "Rechazar"
2. La cotización cambia visualmente a "rechazada"
3. Si ya hay una aceptada, los botones de las demás quedan deshabilitados

### 8. Valoración

**Decisión:** Formulario con 5 criterios de 1-5, promedio calculado con computed().

**Criterios:**
- Puntualidad
- Calidad
- Trato
- Limpieza
- Cumplimiento del precio

**Controles:**
- Select o botones numéricos simples (1-5) por criterio
- Campo de comentario opcional
- Checkbox "Volvería a contratar"
- Promedio calculado en tiempo real

**Flujo:**
1. Usuario califica cada criterio
2. Promedio se actualiza automáticamente
3. Usuario envía valoración
4. Se muestra mensaje de confirmación
5. Botón para volver a /panel-cliente

### 9. Navegación

**Decisión:** Flujo de navegación lineal entre pantallas cliente.

```
solicitud-servicio → [confirmación] → panel-cliente
panel-cliente → "Ver detalle" → detalle-solicitud
detalle-solicitud → "Aceptar cotización" → [en_proceso]
detalle-solicitud → botón prueba → valorar-servicio
valorar-servicio → [confirmación] → panel-cliente
```

**Nota:** El botón "Solicitar servicio" del perfil técnico mantiene navegación a `/login` por ahora.

### 10. Estilos CSS

**Decisión:** Usar CSS estándar con clases convencionales, consistente con el patrón existente.

**Rationale:** Sin preprocesadores, sin dependencias externas.

## Risks / Trade-offs

- **[Trade-off]** Datos duplicados entre componentes → **Mitigación:** Aceptable para caso académico; se puede refactorear a servicio compartido después
- **[Trade-off]** Patrón mixto (Signals vs propiedades plain) → **Mitigación:** Temporal; se puede estandarizar en futuro
- **[Riesgo]** Sin autenticación: pantallas accesibles por URL → **Mitigación:** Aceptable para fase de desarrollo visual
- **[Limitación]** Sin :id en rutas: no se simula selección de solicitud específica → **Mitigación:** Cada pantalla muestra datos fijos simulados

## Open Questions

(Ninguna - todas las decisiones fueron respondidas)
