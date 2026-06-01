## Why

El frontend ya tiene layout base, pantallas públicas, flujo cliente y flujo técnico, pero el panel administrador (`/panel-administrador`) sigue siendo un placeholder. Este cambio implementa visualmente las funciones de gestión del administrador con datos simulados y Angular Signals, completando los tres roles del prototipo académico.

## What Changes

- Implementar `panel-administrador` como único componente con secciones apiladas y scroll vertical (sin subcomponentes ni pestañas).
- Resumen general con grid de 6 contadores computed (técnicos totales/pendientes/validados/rechazados, categorías, usuarios).
- Gestión visual de técnicos en lista única con badge; validar/rechazar solo `pendiente`; mensaje breve de confirmación.
- Gestión de categorías con nomenclatura del flujo cliente; formulario agregar con validación de duplicados.
- 5 usuarios simulados con rol y estado (activo/pendiente/rechazado).
- Reportes básicos con métricas fijas narrativas y computed donde aplique.
- Signals: `tecnicos`, `categorias`, `usuarios`, `reportes`, `formCategoria`, `mensajeAccion`.
- Crear `panel-administrador.css` responsive.

## Capabilities

### New Capabilities

- `admin-dashboard`: Panel del administrador con resumen, validación de técnicos, categorías, usuarios y reportes simulados gestionados con Signals.

### Modified Capabilities

- _(ninguna)_

## Impact

- **Frontend:** solo `components/panel-administrador/` (`.ts`, `.html`, `.css`).
- **Sin impacto** en rutas, models, services, backend ni otros componentes.
- **Coherencia narrativa:** Carlos Mendoza validado; Rosa Huamán pendiente (evita conflicto con Ana Ruiz); sin Roberto Salas rechazado.
- **Sin sincronización** entre paneles en runtime (mocks independientes).
