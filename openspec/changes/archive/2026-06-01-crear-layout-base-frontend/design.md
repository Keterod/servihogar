## Context

El frontend de ServiHogar (`servihogar-frontend/`) usa Angular 21 con componentes standalone. Actualmente `app.html` contiene únicamente `<router-outlet />`, las rutas están definidas en `app.routes.ts` (10 rutas), y los componentes de página son placeholders sin contenido visual. No hay estilos globales (`styles.css` está vacío) ni navegación entre rutas.

Este es el primer sprint visual del frontend académico. Las restricciones exigen código simple, sin librerías externas, sin auth y sin tocar models/services.

## Goals / Non-Goals

**Goals:**

- Proporcionar un shell visual persistente: navbar + contenido (router-outlet) + footer.
- Habilitar navegación pública entre Inicio, Buscar técnicos e Iniciar sesión mediante `routerLink`.
- Establecer estilos globales mínimos con CSS puro y variables CSS.
- Lograr layout vertical responsive básico (navbar adaptable en pantallas pequeñas).
- Mantener compatibilidad con Angular 21 y componentes standalone.

**Non-Goals:**

- Autenticación, guards de ruta o lógica de sesión.
- Conexión con backend FastAPI.
- Contenido de negocio en las páginas existentes.
- Links a paneles (cliente, técnico, administrador) en el navbar.
- Menú hamburguesa, tema oscuro, i18n o librerías UI.
- Uso de Signals (opcional en sprints futuros).
- Modificación de `models/` o `services/`.

## Decisions

### 1. Shell en `app.html` (no `MainLayout` con rutas hijas)

**Decisión:** Integrar navbar, `<main>` con router-outlet y footer directamente en `app.html`, importando los componentes en `app.ts`.

**Alternativa descartada:** Componente `MainLayout` con rutas anidadas como children. Es más escalable para layouts diferenciados (p. ej. login sin navbar), pero añade complejidad innecesaria en este sprint.

**Rationale:** Menor número de archivos y conceptos; adecuado para proyecto académico. Un sprint futuro puede extraer `MainLayout` cuando se implemente auth.

### 2. Componentes standalone en `components/`

**Decisión:** Crear `components/navbar/` y `components/footer/` como componentes standalone con sus propios `.ts`, `.html` y `.css`.

**Rationale:** Sigue la estructura existente del proyecto (`components/home/`, etc.) sin introducir carpetas nuevas (`layouts/`, `shared/`).

### 3. Navegación con `RouterLink` y `RouterLinkActive`

**Decisión:** El navbar importa `RouterLink` y `RouterLinkActive` de `@angular/router`. Enlaces:

| Texto | Ruta |
|-------|------|
| Inicio | `/inicio` |
| Buscar técnicos | `/buscar-tecnicos` |
| Iniciar sesión | `/login` |

Estado activo con clase CSS `.active` vía `[routerLinkActive]="'active'"`.

**Rationale:** Patrón estándar de Angular Router; navegación SPA sin recarga.

### 4. Estilos globales con variables CSS

**Decisión:** Definir tokens en `:root` dentro de `styles.css`:

- Reset mínimo (`box-sizing`, márgenes de `body`).
- Variables: colores primario/texto/fondo, tipografía system-ui, ancho máximo del contenedor.
- Estilos base para `body`, `a` y clase utilitaria `.container`.

Estilos específicos de navbar y footer en sus archivos `.css` de componente.

**Rationale:** Separación clara entre tokens globales y estilos de componente; sin dependencias externas.

### 5. Layout flex en `app.css`

**Decisión:** `:host` como flex column con `min-height: 100dvh`. El `<main>` crece con `flex: 1` para empujar el footer al fondo en páginas con poco contenido.

**Rationale:** Patrón CSS simple y predecible para sticky footer.

### 6. Responsive básico sin menú hamburguesa

**Decisión:** Navbar con flexbox; en viewports estrechos los links hacen wrap o se apilan. Sin JavaScript adicional.

**Rationale:** Cumple criterio de adaptación básica con mínima complejidad.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Login y paneles comparten el mismo layout con navbar | Aceptable en sprint 1; documentado como evolución futura con `MainLayout` |
| Rutas inválidas muestran layout sin contenido | Fuera de alcance; ruta wildcard 404 en sprint posterior |
| Componentes referencian `.css` inexistentes | No bloquea build; no se modifica en este cambio |
| Navbar expone `/login` sin funcionalidad real | Placeholder coherente con ruta existente; auth en sprint futuro |

## Migration Plan

No aplica migración: cambio aditivo en frontend. Pasos de verificación post-implementación:

1. `npm run build` sin errores.
2. `ng serve` y navegar entre las 3 rutas del navbar.
3. Verificar estado activo del enlace y layout en viewport móvil (~375px).

## Open Questions

- _(ninguna — alcance cerrado por el usuario)_
