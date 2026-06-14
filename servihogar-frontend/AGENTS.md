Eres experto en TypeScript, Angular y desarrollo web escalable. Escribes código funcional, mantenible, performante y accesible siguiendo las mejores prácticas de Angular y TypeScript.

## TypeScript

- Usar comprobación estricta de tipos.
- Preferir inferencia de tipos cuando el tipo sea obvio.
- Evitar `any`; usar `unknown` cuando el tipo sea incierto.

## Angular — reglas generales

- Usar **componentes standalone**; no crear NgModules para pantallas nuevas.
- Angular moderno maneja standalone como valor por defecto. Preferir omitir `standalone: true`, pero se permite declararlo explícitamente cuando el Angular Language Service, el IDE o el build lo requiera para resolver imports de forma estática.
- Usar **Angular Signals** para estado local en componentes con formularios, filtros, listas simuladas y datos derivados.
- No basta con declarar Signals sueltas sin patrón: los **formularios interactivos** deben manejarse con Signals (ver sección «Formularios con Signals»).
- Signal Forms puede evaluarse más adelante; en este proyecto el patrón por defecto es `signal` + `computed`.
- Implementar **Lazy Loading obligatorio** en rutas de pantallas con `loadComponent`.
- No usar `@HostBinding` ni `@HostListener`; usar el objeto `host` en el decorador.
- Usar `NgOptimizedImage` para imágenes estáticas cuando existan assets reales.

## Arquitectura y estructura

- **components/**: pantallas y componentes visuales. Cada componente debe tener su `.html`, `.ts` y `.css` cuando aplique.
- **services/**: lógica de negocio y futura comunicación con backend/Supabase.
- **models/**: interfaces TypeScript para estructurar los datos del dominio.

No mezclar responsabilidades: la UI vive en componentes; la persistencia y APIs en servicios.

## Estilo visual — Bootstrap (obligatorio)

- **Bootstrap es obligatorio** como toolkit visual del proyecto.
- Bootstrap debe incluirse **por CDN** en el archivo principal HTML del frontend.
- No instalar Bootstrap por npm ni configurarlo mediante `angular.json`, salvo indicación explícita posterior.
- Usar utilidades, grid y componentes de Bootstrap cuando mejoren consistencia y velocidad de desarrollo.
- El **CSS propio** solo debe **complementar** Bootstrap: branding, ajustes visuales y detalles específicos del prototipo.
- No reescribir toda la UI solo con CSS custom si Bootstrap resuelve el layout o el patrón de componente.
- No agregar otros frameworks UI salvo aprobación explícita.

## Base de datos — Supabase

- La base de datos se gestiona **únicamente con [Supabase](https://supabase.com/)** (PostgreSQL administrado en la nube).
- **No se requiere** PostgreSQL local para desarrollar el frontend.
- **Supabase Auth** maneja correo, contraseña e inicio de sesión (integración real pendiente según fase del proyecto).
- **Supabase Storage** almacena imágenes y documentos; la BD guarda rutas/URLs de referencia.
- Archivos principales del esquema (en la raíz del repo):
  - `database/schema.sql`
  - `database/seed.sql`
  - `database/README.md`
- El frontend actual puede usar **datos simulados en memoria** hasta que se conecte Supabase y el backend; no inventar integraciones que aún no existen.

## Routing y Lazy Loading (obligatorio)

- El proyecto **debe** usar Lazy Loading en rutas de pantallas.
- Las rutas deben cargarse con **`loadComponent`**.
- **No** importar componentes de página de forma eager en `app.routes.ts` si pueden cargarse de forma diferida.

Ejemplo:

```ts
export const routes: Routes = [
  {
    path: 'inicio',
    loadComponent: () => import('./components/home/home').then((m) => m.Home),
  },
  {
    path: 'buscar-tecnicos',
    loadComponent: () =>
      import('./components/buscar-tecnicos/buscar-tecnicos').then((m) => m.BuscarTecnicos),
  },
];
```

## Formularios con Signals

Los formularios interactivos **no** deben manejarse con objetos mutables simples (`this.form = { ... }` y asignaciones directas).

Patrón obligatorio para formularios locales:

- `signal({ ... })` para el estado del formulario.
- `computed()` para validaciones, totales, filtros y botón deshabilitado.
- `update()` (o `set()`) para cambiar campos.
- **No** usar `mutate()` en signals.

```ts
readonly form = signal({
  nombre: '',
  correo: '',
  mensaje: '',
});

readonly puedeEnviar = computed(() => {
  const value = this.form();

  return (
    value.nombre.trim() !== '' &&
    value.correo.trim() !== '' &&
    value.mensaje.trim() !== ''
  );
});

actualizarCampo(campo: 'nombre' | 'correo' | 'mensaje', valor: string): void {
  this.form.update((actual) => ({
    ...actual,
    [campo]: valor,
  }));
}
```

Template:

```html
<input [value]="form().nombre" (input)="actualizarCampo('nombre', $any($event.target).value)" />

<button type="button" [disabled]="!puedeEnviar()">Enviar</button>
```

Usar `computed()` también para: filtros, contadores, promedios, elemento seleccionado, etiquetas formateadas y estados derivados en paneles.

## Gestión de estado

- Signals para estado local del componente.
- `computed()` para estado derivado.
- Transformaciones de estado puras y predecibles.
- No usar `mutate`; preferir `update()` o `set()`.

## Componentes

- Componentes pequeños y con una sola responsabilidad.
- Preferir `input()` y `output()` en lugar de decoradores `@Input` / `@Output`.
- `changeDetection: ChangeDetectionStrategy.OnPush` en `@Component` cuando aplique.
- Plantillas inline solo para componentes muy pequeños.
- No usar `ngClass`; usar bindings `class`.
- No usar `ngStyle`; usar bindings `style`.
- Templates y estilos externos con rutas relativas al archivo `.ts` del componente.

## Plantillas

- Plantillas simples; evitar lógica compleja en HTML.
- Control flow nativo: `@if`, `@for`, `@switch` (no `*ngIf`, `*ngFor`, `*ngSwitch`).
- Usar `async` pipe para observables cuando existan.
- No asumir globals como `new Date()` disponibles en plantilla.

## Servicios

- Un servicio, una responsabilidad principal.
- `providedIn: 'root'` para singletons.
- Preferir `inject()` frente a inyección por constructor cuando encaje con el estilo del proyecto.

## Accesibilidad

- Debe pasar comprobaciones AXE en pantallas revisadas.
- Cumplir mínimos WCAG AA: foco, contraste, ARIA cuando corresponda.

## Restricciones del prototipo académico

- No conectar backend ni Supabase sin que la tarea lo pida explícitamente.
- No implementar autenticación real en el frontend hasta la fase de integración.
- Mantener mocks y Signals locales mientras el flujo sea solo demostración visual.
- No modificar `database/schema.sql` ni `database/seed.sql` desde tareas de frontend salvo indicación explícita.
