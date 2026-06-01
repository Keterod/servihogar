## 1. Estado y datos simulados (panel-tecnico.ts)

- [x] 1.1 Definir interfaces locales: Tecnico, Solicitud, CotizacionEnviada, ServicioAceptado, FormCotizacion
- [x] 1.2 Crear `tecnico = signal(...)` — Carlos Mendoza, Gasfitería menor, Huancayo Centro, 4.8
- [x] 1.3 Crear `estadoValidacion = signal('validado')`
- [x] 1.4 Crear `solicitudesDisponibles = signal([...])` — ids 2 y 3 (Gasfitería menor); excluir id 1
- [x] 1.5 Crear `cotizacionesEnviadas = signal([...])` — precarga cotización id 1 Carlos (pendiente), alineada con detalle-solicitud
- [x] 1.6 Crear `serviciosAceptados = signal([...])` — al menos un servicio simulado
- [x] 1.7 Crear `solicitudSeleccionada = signal<Solicitud | null>(null)`
- [x] 1.8 Crear `formCotizacion = signal({ precio: '', tiempo: '', propuesta: '' })`
- [x] 1.9 Crear computed: totalSolicitudesDisponibles, totalCotizacionesEnviadas, totalServiciosAceptados, puedeEnviarCotizacion

## 2. Lógica de interacción

- [x] 2.1 Implementar seleccionarSolicitud(solicitud): actualizar solicitudSeleccionada y resetear formCotizacion
- [x] 2.2 Implementar enviarCotizacion(): validar precio > 0, campos no vacíos, técnico validado; agregar a enviadas; remover de disponibles; limpiar formulario y selección
- [x] 2.3 Implementar helpers: getEstadoValidacionLabel, getEstadoValidacionClass, getEstadoCotizacionLabel, formatPrecio (S/)

## 3. Vista (panel-tecnico.html)

- [x] 3.1 Sección header: resumen técnico + badge validación (validado en demo)
- [x] 3.2 Sección resumen: contadores computed
- [x] 3.3 Sección solicitudes disponibles: tarjetas clicables con estilo activo al seleccionar
- [x] 3.4 Sección detalle de solicitud seleccionada + formulario (precio S/, tiempo, propuesta)
- [x] 3.5 Botón enviar cotización deshabilitado si !puedeEnviarCotizacion()
- [x] 3.6 Sección cotizaciones enviadas: tarjetas con todos los campos requeridos
- [x] 3.7 Sección servicios aceptados: tarjetas con categoría, descripción, zona, cliente, estado, fecha

## 4. Estilos (panel-tecnico.css)

- [x] 4.1 Tarjetas, resumen, formulario y badges — patrón coherente con panel-cliente
- [x] 4.2 Estilo `.activa` / borde para solicitud seleccionada
- [x] 4.3 Responsive ~375px, scroll vertical

## 5. Verificación

- [x] 5.1 `npm run build` sin errores
- [x] 5.2 Solicitud id 1 NO en disponibles; SÍ en cotizaciones enviadas (pendiente)
- [x] 5.3 Cotizar solicitud id 2 o 3: desaparece de disponibles, aparece en enviadas
- [x] 5.4 Cambiar selección sin enviar limpia formulario
- [x] 5.5 Solo Gasfitería menor en disponibles; zona técnico Huancayo Centro
- [x] 5.6 Signals y computed presentes en panel-tecnico.ts
- [x] 5.7 Responsive básico en viewport ~375px
