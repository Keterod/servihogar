## Why

El frontend de ServiHogar ya tiene el layout base y las pantallas públicas funcionando, pero falta implementar el flujo visual del cliente que permite solicitar servicios, ver cotizaciones y valorar el trabajo realizado. Este cambio establece las pantallas del cliente usando Angular 21 y Signals para manejo de estado local, sin conexión al backend, permitiendo validar visualmente el flujo completo del cliente antes de integrar servicios reales.

## What Changes

- Implementar contenido visual en las 4 pantallas del cliente existentes (solicitud, panel, detalle, valoración)
- Usar Angular Signals para estado local solo en componentes del flujo cliente
- Mantener componentes en sus ubicaciones actuales sin reubicar
- Mantener rutas sin parámetros (:id)
- Datos simulados coherentes entre pantallas
- No se modifica el backend, no se agregan dependencias, no se migran pantallas públicas

## Capabilities

### New Capabilities

- `client-service-request`: Formulario visual para publicar solicitudes de servicio con Signals para manejo de estado local del formulario
- `client-dashboard`: Panel del cliente con resumen de solicitudes simuladas usando Signals y computed
- `client-request-detail`: Detalle de solicitud con cotizaciones simuladas y Signals para representar cotización aceptada
- `client-service-rating`: Pantalla de valoración del servicio finalizado con Signals para criterios de evaluación

### Modified Capabilities

(ninguna - se mantiene el perfil técnico con navegación a /login por ahora)

## Impact

- Frontend Angular: Componentes existentes en `src/app/components/solicitud-servicio/`, `panel-cliente/`, `detalle-solicitud/`, `valorar-servicio/`
- Rutas: Sin cambios - rutas actuales sin parámetros
- Datos: Datos simulados dentro de cada componente, coherentes entre pantallas
- Estado: Uso de Angular Signals para estado local solo en estos 4 componentes
- No se modifica el backend existente
- No se agregan dependencias externas
- No se migran componentes de pantallas públicas a Signals
