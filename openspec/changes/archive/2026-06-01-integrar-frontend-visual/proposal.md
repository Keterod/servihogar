## Why

Los cinco flujos del frontend académico ya están implementados, pero fueron desarrollados en sprints separados con estilos, textos y espaciados heterogéneos. Antes de entregar capturas o evidencias del informe, hace falta una pasada de integración visual moderada que unifique la presentación, facilite la navegación de prueba entre roles y alinee textos y categorías con el vocabulario del informe y la base de datos, sin tocar lógica funcional ni conectar backend.

## What Changes

- Extender `styles.css` con utilidades compartidas (botones, tarjetas, badges, grids, contenedores) y migrar progresivamente duplicados evidentes a tokens globales — sin refactorización grande.
- Footer como **única** ubicación de accesos demo: texto "Acceso demo (prototipo académico)" con links a panel cliente, técnico y administrador; visibles en **todas** las rutas; navbar público sin cambios.
- Home: hero breve con flujo completo; 5 pasos (incluye valoración); categorías con nomenclatura oficial (Gasfitería menor, Electricidad básica, Mantenimiento de computadoras, Pintura básica, Armado de muebles).
- Perfil público de Carlos Mendoza: Gasfitería menor, Huancayo Centro.
- Búsqueda de técnicos: alinear filtros y mocks principales con las categorías definidas cuando sea sencillo.
- Ajustes visuales moderados en pantallas prioritarias para capturas del informe (10 pantallas listadas).
- Badges: unificar apariencia (colores/tamaños) vía tokens; **no** renombrar clases existentes.
- Botones: mover estilos comunes a global y eliminar duplicados locales solo si no rompe diseño.
- CSS budget: mover duplicados simples a global; **no** subir `maximumWarning` en `angular.json`; warning menor aceptable si build pasa.
- Coherencia narrativa: Carlos Mendoza validado / Gasfitería menor; Roberto Salas solo cotizando en detalle-solicitud; evitar "Fontanería" donde pueda reemplazarse.

## Capabilities

### New Capabilities

- `frontend-visual-integration`: Integración visual transversal — utilidades globales progresivas, coherencia textual, responsive, mitigación CSS budget y reglas de coherencia narrativa entre mocks.

### Modified Capabilities

- `frontend-layout`: Accesos demo en footer (texto exacto, todas las rutas); extensión de estilos globales compartidos; navbar sin paneles.
- `frontend-public-screens`: Home (hero, 5 pasos, categorías), perfil técnico Carlos Mendoza, búsqueda alineada con categorías del sistema.

## Impact

- **Frontend:** `styles.css`, `app.css`, `footer`, `home`, `buscar-tecnicos`, `perfil-tecnico`, `login-register`, flujo cliente (CSS/HTML), tres paneles (CSS/tokens/textos simples).
- **Sin impacto** en rutas, models, services, backend, Signals ni lógica de negocio.
- **Mocks no sincronizados** entre pantallas — aceptado (sin backend ni estado global).
- **Sin nuevas dependencias** ni autenticación real.
