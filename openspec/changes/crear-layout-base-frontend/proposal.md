## Why

ServiHogar ya tiene rutas y componentes placeholder, pero la aplicación se renderiza sin marco visual común ni navegación usable. Este cambio establece el layout base del frontend para que todas las pantallas compartan navbar y footer, con estilos globales mínimos, como primer sprint visual del proyecto académico.

## What Changes

- Crear componente standalone `Navbar` con enlaces públicos: Inicio, Buscar técnicos e Iniciar sesión.
- Crear componente standalone `Footer` con contenido estático del proyecto.
- Integrar Navbar, `<router-outlet>` y Footer en `app.html` como shell de la aplicación.
- Agregar estilos globales básicos en `styles.css` (reset mínimo, variables CSS, tipografía y contenedor).
- Ajustar `app.css` para layout vertical con contenido principal flexible (`flex` column, footer al final).
- Actualizar `index.html`: idioma español (`lang="es"`) y título "ServiHogar".
- Los paneles de cliente, técnico y administrador permanecen accesibles solo por URL; no aparecen en el navbar.

## Capabilities

### New Capabilities

- `frontend-layout`: Shell visual de la aplicación (navbar, área de contenido con router-outlet, footer), estilos globales base, navegación pública entre rutas y adaptación responsive básica.

### Modified Capabilities

- _(ninguna — no existen specs previas en el repositorio)_

## Impact

- **Frontend (`servihogar-frontend/`)**: nuevos componentes en `src/app/components/navbar/` y `src/app/components/footer/`; modificaciones en `app.ts`, `app.html`, `app.css`, `styles.css` e `index.html`.
- **Sin impacto** en `models/`, `services/`, backend, base de datos ni dependencias npm.
- **Rutas existentes** en `app.routes.ts` se mantienen; el layout envuelve todas las rutas actuales sin cambiar su definición.
