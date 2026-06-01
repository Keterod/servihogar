## Why

El frontend ya tiene layout base, pantallas públicas y flujo del cliente, pero el panel del técnico (`/panel-tecnico`) sigue siendo un placeholder. Este cambio implementa visualmente el flujo del técnico con datos simulados y Angular Signals, alineado con el modelo de negocio donde el técnico revisa solicitudes de su especialidad y envía cotizaciones.

## What Changes

- Implementar `panel-tecnico` como **único componente** con secciones apiladas y scroll vertical (sin subcomponentes ni pestañas).
- Resumen del técnico Carlos Mendoza (gasfitería/fontanería, Huancayo Centro, validado).
- Solicitudes disponibles como **tarjetas** (patrón `panel-cliente`), solo **Gasfitería menor**; ids 1, 2 y 3 coherentes con el universo cliente.
- Solicitud id 1 (Fuga de agua en cocina) **excluida** de disponibles — Carlos ya cotizó; aparece en cotizaciones enviadas.
- Formulario de cotización: precio estimado (S/), tiempo estimado, propuesta; validación mínima; una cotización por solicitud.
- Cotizaciones enviadas y servicios aceptados como tarjetas con estados definidos.
- Estado de validación visible (`pendiente`, `validado`, `rechazado`); demo con `validado`.
- Signals locales: `tecnico`, listas, `solicitudSeleccionada`, `formCotizacion`; `computed()` para contadores y `puedeEnviarCotizacion`.
- Crear `panel-tecnico.css` responsive.

## Capabilities

### New Capabilities

- `technician-dashboard`: Panel del técnico con resumen, solicitudes disponibles filtradas por especialidad, cotización visual con Signals, cotizaciones enviadas, servicios aceptados y estado de validación.

### Modified Capabilities

- _(ninguna)_

## Impact

- **Frontend:** solo `components/panel-tecnico/` (`.ts`, `.html`, `.css`).
- **Sin impacto** en rutas, models, services, backend, navbar ni otros componentes.
- **Coherencia narrativa** con flujo cliente (ids 1–3, Huancayo, Gasfitería); sin estado compartido en runtime.
- **Sin nuevas dependencias** ni autenticación real.
