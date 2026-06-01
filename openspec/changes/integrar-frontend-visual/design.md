## Context

ServiHogar es un frontend Angular 21 académico con cinco flujos archivados. CSS local usa colores hardcodeados mezclados con tokens en `styles.css`. Navbar público: Inicio, Buscar técnicos, Iniciar sesión. Paneles accesibles por URL. Build advierte CSS budget en `panel-tecnico.css` y `panel-administrador.css` (~4.2–4.5 kB vs warning 4 kB).

Vocabulario oficial de categorías (informe / BD):
1. Gasfitería menor
2. Electricidad básica
3. Mantenimiento de computadoras
4. Pintura básica
5. Armado de muebles

## Goals / Non-Goals

**Goals:**

- Integración visual **moderada** en pantallas prioritarias para capturas del informe.
- Utilidades globales en `styles.css`; migración **progresiva** de duplicados evidentes.
- Footer único con accesos demo visibles en todas las rutas.
- Textos y categorías alineados al flujo: publicar → cotizar → aceptar → valorar.
- Carlos Mendoza coherente: Gasfitería menor, Huancayo Centro, validado en panel técnico.
- CSS budget: refactor simple a global; warning menor aceptable.

**Non-Goals:**

- Refactorización grande, rediseño completo, renombrar clases badge.
- Barra fija, bloque demo en login, sección demo en home.
- Accesos demo a solicitud-servicio, detalle-solicitud, valorar-servicio.
- Cambios en navbar, rutas, models, services, backend, auth real, librerías.
- Sincronizar mocks entre pantallas en runtime.
- Subir `maximumWarning` en `angular.json`.
- Modificar specs archivadas.

## Decisions

### 1. Accesos demo — footer único

```
© 2026 ServiHogar — Proyecto académico
Acceso demo (prototipo académico)
Panel cliente · Panel técnico · Panel administrador
```

- Visible en **todas** las rutas, incluidos paneles.
- Solo tres links de rol; sin links al flujo cliente intermedio.
- Estilo secundario (`--color-muted`, texto pequeño).
- Navbar **sin cambios**.

### 2. Utilidades globales — migración progresiva

Agregar en `styles.css`:

| Utilidad | Propósito |
|----------|-----------|
| `.btn-primary`, `.btn-secondary` | CTAs compartidos |
| `.card` | Tarjetas base |
| `.section-header` | Títulos de sección |
| `.resumen-grid`, `.resumen-item`, … | Contadores en paneles |
| Tokens badge (colores compartidos) | Apariencia unificada sin renombrar clases |

**Enfoque:** añadir global → migrar duplicados **solo cuando sea sencillo** → eliminar local **solo si no rompe diseño**. No refactor masivo.

### 3. Badges — apariencia, no nombres

Mantener clases existentes:
- `panel-cliente`: `.solicitud-estado[data-estado]`
- `panel-tecnico`: `.badge-validacion`, `.estado-badge`
- `panel-administrador`: `.badge-validacion`, `.badge-rol`, `.badge-estado-usuario`

Unificar **colores, tamaños y bordes** vía tokens CSS o reglas globales que apunten a selectores existentes. No renombrar HTML salvo riesgo bajo.

### 4. Contenedores

- `.container` global (1100px) como referencia principal.
- Paneles pueden mantener `.container` local con distinto `max-width` (800px, 900px) si mejora lectura.

### 5. Pantallas prioritarias (capturas informe)

1. `/inicio`
2. `/buscar-tecnicos`
3. `/perfil-tecnico`
4. `/login`
5. `/solicitud-servicio`
6. `/panel-cliente`
7. `/detalle-solicitud`
8. `/valorar-servicio`
9. `/panel-tecnico`
10. `/panel-administrador`

Ajustes moderados: tokens, espaciado, responsive ~375px. Sin rediseño.

### 6. Home

**Hero** (breve): mencionar publicar solicitudes, recibir cotizaciones y valorar al finalizar.

**Categorías destacadas:** las 5 categorías oficiales (evitar "Fontanería").

**Pasos (5):**
1. Busca técnicos
2. Revisa perfiles
3. Publica una solicitud
4. Elige una cotización
5. Valora el servicio al finalizar

**Layout pasos:** grid en desktop, lista vertical en móvil (~375px).

### 7. Perfil técnico y búsqueda

**perfil-tecnico** (Carlos Mendoza):
- Especialidad: Gasfitería menor
- Zona: Huancayo Centro
- Descripción/servicios: vocabulario acorde (sin "fontanería" si puede evitarse)

**buscar-tecnicos:**
- Filtro categorías: las 5 oficiales (+ opción "Todas")
- Carlos Mendoza: Gasfitería menor, Huancayo Centro (o zona coherente con filtros)
- Ajustar mocks secundarios a categorías definidas cuando sea cambio de texto simple
- Mantener lógica de filtrado in-memory; no rehacer componente

### 8. Coherencia narrativa

| Regla | Acción |
|-------|--------|
| Carlos Mendoza | Gasfitería menor, Huancayo Centro, validado en panel técnico |
| Roberto Salas | Solo en detalle-solicitud cotizando; no mostrarlo rechazado en admin |
| Ana Ruiz | Solo en búsqueda pública; sin conflicto cross-panel → mantener o renombrar solo si surge contradicción |
| Fontanería | Reemplazar por Gasfitería menor en textos visibles donde sea sencillo |
| Mocks entre pantallas | No sincronizados — aceptado |

### 9. CSS budget

1. Mover duplicados simples (`.btn-primary`, `.resumen-*`, colores repetidos) a `styles.css`.
2. Podar reglas muertas en paneles.
3. **No** modificar `angular.json` budgets.
4. Warning residual aceptable si build sin errores (error threshold 8 kB).

### 10. Archivos permitidos

- `.css`, `.html`, textos estáticos en `.ts` (arrays, strings de mock visible).
- **Prohibido:** lógica Signals, models, services, routes, backend.

## Risks / Trade-offs

- **[Risk] Regresión visual al mover `.btn-primary`** → Migrar uno a uno; conservar variantes `:disabled`, `.confirmacion`.
- **[Risk] Budget warning persiste** → Aceptado; no subir config.
- **[Risk] Filtros búsqueda vs mocks** → Actualizar mocks y filtros juntos en un solo paso textual.
- **[Trade-off] Mocks no sincronizados** → Documentado; coherencia visual > consistencia runtime.

## Migration Plan

1. `styles.css` — utilidades y tokens badge.
2. Footer — accesos demo.
3. Home — hero, categorías, 5 pasos, layout responsive.
4. Perfil técnico + buscar técnicos — textos y filtros.
5. Paneles — tokens + dedup CSS moderado.
6. Flujo cliente + login — tokens y botones duplicados.
7. `npm run build` + revisión manual de 10 pantallas.

## Open Questions

- _(ninguna — decisiones confirmadas por el usuario)_
