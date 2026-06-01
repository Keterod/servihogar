## 1. Solicitud de Servicio

- [x] 1.1 Implementar formulario con 6 campos: categoría (select), zona (select), descripción (textarea), fecha tentativa (date), horario preferido (select/texto), dirección (texto)
- [x] 1.2 Definir opciones simuladas: categorías (Gasfitería menor, Electricidad básica, etc.) y zonas (Huancayo Centro, El Tambo, etc.)
- [x] 1.3 Crear Signals para cada campo del formulario
- [x] 1.4 Agregar botón "Publicar solicitud" con mensaje de confirmación visual
- [x] 1.5 Agregar botón de navegación a `/panel-cliente` después de confirmar
- [x] 1.6 Implementar HTML del formulario en `solicitud-servicio.html`
- [x] 1.7 Implementar estilos CSS del formulario en `solicitud-servicio.css`

## 2. Panel del Cliente

- [x] 2.1 Definir array de 3 solicitudes simuladas con datos coherentes (Gasfitería menor, Huancayo Centro, etc.)
- [x] 2.2 Crear Signal para la lista de solicitudes
- [x] 2.3 Crear computed() para contar estados: pendiente, en_proceso, finalizado, cancelado
- [x] 2.4 Implementar HTML para mostrar lista de solicitudes con categoría, descripción, zona, fecha, estado, cotizaciones
- [x] 2.5 Agregar botón "Ver detalle" que navegue a `/detalle-solicitud`
- [x] 2.6 Implementar estilos CSS del panel en `panel-cliente.css`

## 3. Detalle de Solicitud

- [x] 3.1 Definir solicitud simulada con 3 cotizaciones (Carlos Mendoza, Luis Arango, Roberto Salas)
- [x] 3.2 Crear Signal para cotización aceptada/seleccionada
- [x] 3.3 Implementar HTML para mostrar información de la solicitud (categoría, descripción, estado, fecha, zona, dirección)
- [x] 3.4 Implementar HTML para mostrar lista de cotizaciones con nombre, especialidad, calificación, precio, tiempo, propuesta, estado
- [x] 3.5 Agregar botón "Aceptar" que actualice el Signal y marque cotización como aceptada
- [x] 3.6 Agregar botón "Rechazar" que marque cotización como rechazada
- [x] 3.7 Implementar lógica: al aceptar, las demás cotizaciones quedan rechazadas o deshabilitadas
- [x] 3.8 Mostrar mensaje de confirmación al aceptar
- [x] 3.9 Cambiar estado de solicitud a "en_proceso" al aceptar
- [x] 3.10 Agregar botón de prueba para navegar a `/valorar-servicio`
- [x] 3.11 Implementar estilos CSS del detalle en `detalle-solicitud.css`

## 4. Valoración del Servicio

- [x] 4.1 Implementar formulario con 5 criterios: puntualidad, calidad, trato, limpieza, cumplimiento del precio
- [x] 4.2 Crear Signal para cada criterio de calificación (1-5)
- [x] 4.3 Crear computed() para promedio calculado
- [x] 4.4 Implementar controles de calificación (select o botones numéricos 1-5)
- [x] 4.5 Agregar campo de comentario opcional (textarea)
- [x] 4.6 Agregar checkbox "Volvería a contratar"
- [x] 4.7 Agregar botón "Enviar valoración" con mensaje de confirmación
- [x] 4.8 Agregar botón de navegación a `/panel-cliente` después de confirmar
- [x] 4.9 Mostrar estado del servicio como "Finalizado"
- [x] 4.10 Implementar estilos CSS de la valoración en `valorar-servicio.css`

## 5. Verificación Final

- [x] 5.1 Compilar proyecto con Angular 21 sin errores
- [x] 5.2 Verificar que las 4 pantallas renderizan correctamente
- [x] 5.3 Verificar Signals funcionan en cada componente
- [x] 5.4 Verificar que no se hacen peticiones HTTP al backend
- [x] 5.5 Verificar navegación: solicitud → confirmación → panel → detalle → aceptar → valorar → panel
- [x] 5.6 Verificar layout responsive en viewport pequeño (375px)
