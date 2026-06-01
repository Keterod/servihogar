## Why

El layout base del frontend ya proporciona navbar, footer y navegación entre rutas, pero las cuatro pantallas públicas principales siguen siendo placeholders sin contenido visual. Este cambio implementa el flujo público básico del sistema (inicio → búsqueda → perfil → login/registro) con datos simulados, alineado con el modelo de negocio de ServiHogar, como segundo sprint visual del proyecto académico.

## What Changes

- Implementar contenido visual de la página de inicio (`home`): propósito de ServiHogar, categorías destacadas y pasos de uso que reflejan el flujo real (buscar → revisar perfiles → publicar solicitud → recibir cotizaciones).
- Implementar pantalla de búsqueda de técnicos (`buscar-tecnicos`): filtros funcionales mínimos en memoria por categoría, zona y calificación, y listado de técnicos simulados.
- Implementar pantalla de perfil del técnico (`perfil-tecnico`): información referencial, especialidad, experiencia, zona, valoración, botón **Solicitar servicio** (navega a `/login`) y texto auxiliar *Inicia sesión como cliente para continuar*.
- Implementar pantalla de iniciar sesión / crear cuenta (`login-register`): una sola pantalla con pestañas visuales (Iniciar sesión / Crear cuenta) y selector de rol (cliente / técnico), sin registro público de administrador.
- Crear archivos CSS faltantes para cada componente afectado.
- Usar datos estáticos o simulados definidos dentro de los componentes (sin backend).
- Mantener rutas existentes y navegación del navbar sin cambios estructurales.

## Capabilities

### New Capabilities

- `frontend-public-screens`: Contenido visual y flujo de navegación de las pantallas públicas (inicio, búsqueda de técnicos, perfil técnico, login/registro) con datos simulados, filtrado en memoria y diseño responsive académico.

### Modified Capabilities

- _(ninguna — `frontend-layout` no cambia sus requisitos)_

## Impact

- **Frontend (`servihogar-frontend/`)**: modificaciones en `components/home/`, `components/buscar-tecnicos/`, `components/perfil-tecnico/` y `components/login-register/` (`.ts`, `.html`, `.css`).
- **Sin impacto** en backend, base de datos, `app.routes.ts`, navbar, footer, `models/` ni `services/`.
- **Sin nuevas dependencias** npm, autenticación real ni conexión con FastAPI.
