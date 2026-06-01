## 1. Estado y datos simulados (panel-administrador.ts)

- [x] 1.1 Definir interfaces: TecnicoAdmin, Categoria, Usuario, FormCategoria, Reportes
- [x] 1.2 Crear `tecnicos = signal([...])` — Carlos validado, Luis/Rosa pendientes, Pedro rechazado; incluir fechaRegistro; sin Roberto Salas
- [x] 1.3 Crear `categorias = signal([...])` — 5 categorías nomenclatura cliente (Gasfitería menor, etc.)
- [x] 1.4 Crear `usuarios = signal([...])` — 5 usuarios con rol y estado
- [x] 1.5 Crear `reportes = signal({ solicitudesPublicadas, cotizacionesRegistradas, serviciosFinalizados })`
- [x] 1.6 Crear `formCategoria = signal({ nombre: '', descripcion: '' })` y `mensajeAccion = signal('')`
- [x] 1.7 Crear computed: totalTecnicos, tecnicosPendientes, tecnicosValidados, tecnicosRechazados, totalCategorias, totalUsuarios, tecnicosActivos, puedeAgregarCategoria

## 2. Lógica de interacción

- [x] 2.1 Implementar `validarTecnico(id)` y `rechazarTecnico(id)` — solo pendiente; actualizar mensajeAccion
- [x] 2.2 Implementar `agregarCategoria()` — validar nombre no vacío, no duplicado; append y limpiar formulario
- [x] 2.3 Implementar helpers: getEstadoValidacionLabel/Class, getRolLabel, getEstadoUsuarioLabel

## 3. Vista (panel-administrador.html)

- [x] 3.1 Header: título panel administrador
- [x] 3.2 Resumen: grid 6 contadores computed
- [x] 3.3 Mensaje acción breve (validar/rechazar) vía mensajeAccion
- [x] 3.4 Técnicos: lista única con badge; botones solo en pendientes; campos id, nombre, especialidad, zona, estado, fechaRegistro
- [x] 3.5 Categorías: listado + formulario (nombre obligatorio, descripción opcional); mensaje duplicado
- [x] 3.6 Usuarios: 5 tarjetas con nombre, rol, estado
- [x] 3.7 Reportes: 5 tarjetas (3 fijas + 2 computed)

## 4. Estilos (panel-administrador.css)

- [x] 4.1 Grid resumen 6 contadores; tarjetas coherentes con panel-cliente/panel-tecnico
- [x] 4.2 Badges validación, rol, estado usuario; mensaje acción
- [x] 4.3 Responsive ~375px, scroll vertical

## 5. Verificación

- [x] 5.1 `npm run build` sin errores
- [x] 5.2 Grid 6 contadores; solicitudes/cotizaciones solo en reportes
- [x] 5.3 Validar/rechazar pendiente: estado, contadores, mensaje breve
- [x] 5.4 Agregar categoría; rechazar duplicado por nombre
- [x] 5.5 Carlos validado; sin Roberto Salas; Rosa Huamán pendiente
- [x] 5.6 5 usuarios con rol y estado; 5 reportes visibles
- [x] 5.7 Signals y computed en panel-administrador.ts
- [x] 5.8 Responsive ~375px
