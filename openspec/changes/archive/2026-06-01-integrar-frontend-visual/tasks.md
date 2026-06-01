## 1. Estilos globales (styles.css)

- [x] 1.1 Agregar utilidades compartidas: `.btn-primary`, `.btn-secondary`, `.card`, `.section-header`
- [x] 1.2 Agregar utilidades de resumen: `.resumen-grid`, `.resumen-item`, `.resumen-numero`, `.resumen-label`
- [x] 1.3 Agregar tokens/reglas globales para apariencia unificada de badges (sin renombrar clases en HTML)
- [x] 1.4 Revisar `app.css` para coherencia con layout flex y main-content

## 2. Footer — accesos demo

- [x] 2.1 Actualizar `footer.html`: texto exacto "Acceso demo (prototipo académico)" + links a panel-cliente, panel-tecnico, panel-administrador
- [x] 2.2 Estilizar links demo en `footer.css` (secundario, visible en todas las rutas)
- [x] 2.3 Verificar navbar sin links a paneles y sin cambios en navegación principal

## 3. Home — textos y presentación

- [x] 3.1 Actualizar `home.ts`: 5 categorías oficiales (Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, Armado de muebles)
- [x] 3.2 Actualizar hero en `home.html`/`home.ts`: mención breve de publicar, cotizar y valorar al finalizar
- [x] 3.3 Actualizar `home.ts`: 5 pasos incluyendo "Valora el servicio al finalizar"
- [x] 3.4 Ajustar `home.css`: grid pasos en desktop, vertical en ~375px; tokens globales; migrar `.btn-primary` a global si es seguro

## 4. Perfil técnico y búsqueda

- [x] 4.1 Actualizar `perfil-tecnico.ts`: Carlos Mendoza — Gasfitería menor, Huancayo Centro, descripción coherente
- [x] 4.2 Actualizar `buscar-tecnicos.ts`: filtros con 5 categorías oficiales; Carlos Mendoza alineado
- [x] 4.3 Ajustar mocks secundarios de búsqueda a categorías definidas (cambios textuales simples)
- [x] 4.4 Pulir `perfil-tecnico.css` y `buscar-tecnicos.css`: tokens y responsive moderado

## 5. Flujo cliente y login

- [x] 5.1 `login-register`: placeholder "Ej. Gasfitería menor"; tokens CSS
- [x] 5.2 `solicitud-servicio`, `detalle-solicitud`, `valorar-servicio`: tokens, espaciado; migrar `.btn-primary` duplicado si no rompe diseño
- [x] 5.3 `panel-cliente.css`: tokens globales; mantener clases badge existentes
- [x] 5.4 NO modificar lógica Signals; NO cambiar Roberto Salas en detalle-solicitud

## 6. Paneles — CSS moderado y textos simples

- [x] 6.1 `panel-tecnico.ts`: especialidad "Gasfitería menor" (sin mezcla Fontanería)
- [x] 6.2 `panel-tecnico.css`: mover duplicados simples a global; tokens; no renombrar badges
- [x] 6.3 `panel-administrador.css`: mover duplicados simples a global; tokens
- [x] 6.4 Verificar Carlos validado y Roberto Salas ausente en lista admin

## 7. Verificación

- [x] 7.1 `npm run build` sin errores
- [x] 7.2 Rutas operativas en 10 pantallas prioritarias
- [x] 7.3 Footer demo en todas las rutas; navbar sin paneles; solo 3 links demo
- [x] 7.4 Home: 5 categorías, 5 pasos, hero con flujo completo
- [x] 7.5 Carlos Mendoza coherente en perfil, búsqueda y panel técnico
- [x] 7.6 Badges visualmente consistentes sin renombrar clases
- [x] 7.7 Responsive ~375px en pantallas revisadas
- [x] 7.8 CSS budget: dedup aplicado; warning residual aceptable; angular.json sin cambios
- [x] 7.9 Signals y lógica funcional sin cambios
