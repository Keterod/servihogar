## Context

ServiHogar tiene el layout base implementado (`frontend-layout` archivado): navbar con enlaces públicos, footer, estilos globales en `styles.css` y `router-outlet` en `app.html`. Las rutas `/inicio`, `/buscar-tecnicos`, `/perfil-tecnico` y `/login` existen en `app.routes.ts`, pero sus componentes solo muestran placeholders.

En el modelo de negocio, el **cliente** publica solicitudes de servicio y los **técnicos** envían cotizaciones; la cotización no es una acción del cliente desde el perfil del técnico. Los modelos de dominio (`Tecnico`, `CategoriaServicio`, `Zona`, `SolicitudServicio`, `Cotizacion`) existen en `models/` como interfaces. Los servicios están definidos pero sin conexión backend. Este sprint añade contenido visual y datos simulados locales en los componentes.

## Goals / Non-Goals

**Goals:**

- Presentar las cuatro pantallas públicas con contenido visual claro y coherente con el diseño académico existente.
- Simular el flujo: inicio → buscar técnicos → perfil técnico → login/registro.
- Explicar en la home el flujo real de ServiHogar (búsqueda, perfiles, solicitud, cotizaciones).
- Filtrado funcional mínimo en memoria en búsqueda (categoría, zona, calificación mínima).
- Perfil con CTA **Solicitar servicio** que navega a `/login` con texto auxiliar para el cliente.
- Login/registro en una sola pantalla con pestañas (Iniciar sesión / Crear cuenta) y roles cliente/técnico.
- Mantener responsive básico reutilizando variables CSS globales.

**Non-Goals:**

- Autenticación real, guards o sesión.
- Conexión con FastAPI o uso de services para fetch.
- Implementación de paneles internos, pantalla de solicitud ni cotizaciones.
- Registro o login de administrador.
- Nuevas rutas, librerías externas o modificación de models/services.
- Filtrado avanzado, query params en URL o lógica de negocio compleja.

## Decisions

### 1. Datos simulados como constantes en el componente

**Decisión:** Definir arrays y objetos estáticos directamente en cada `.ts` de componente (p. ej. `TECNICOS_SIMULADOS`, `CATEGORIAS_DESTACADAS`, `PASOS_USO`).

**Alternativa descartada:** Archivo `data/mock-*.ts` compartido o services con datos hardcodeados.

**Rationale:** Máxima simplicidad para proyecto académico; evita tocar `services/` y mantiene cada pantalla autocontenida.

### 2. Navegación interna con `RouterLink`

**Decisión:** Enlaces entre pantallas del flujo público usando `routerLink`:

| Origen | Destino | Acción |
|--------|---------|--------|
| Home | `/buscar-tecnicos` | CTA "Buscar técnicos", categorías |
| Buscar técnicos | `/perfil-tecnico` | Clic en tarjeta de técnico |
| Perfil técnico | `/login` | Botón "Solicitar servicio" |
| Home / navbar | `/login` | Enlace navbar "Iniciar sesión" |

**Rationale:** El CTA del perfil lleva a login porque solicitar servicio requiere sesión de cliente; no se usa `/solicitud-servicio` en este sprint.

### 3. Perfil técnico con ruta fija (sin parámetro de ID)

**Decisión:** Mantener ruta `/perfil-tecnico` sin `:id`. Mostrar un técnico simulado representativo. La búsqueda navega a la misma ruta.

**Rationale:** Evita cambiar `app.routes.ts`; suficiente para prototipo académico.

### 4. CTA del perfil: solo "Solicitar servicio"

**Decisión:** Un único botón con texto **Solicitar servicio**, navegando a `/login`. Texto auxiliar debajo: *Inicia sesión como cliente para continuar*.

**Alternativa descartada:** Botón "Solicitar cotización" — en ServiHogar la cotización la envía el técnico, no el cliente.

**Rationale:** Alineado con el dominio; sin funcionalidad real de solicitud en este sprint.

### 5. Pasos de uso en la home (flujo real)

**Decisión:** Mostrar cuatro pasos informativos:

1. Busca técnicos por categoría y zona.
2. Revisa perfiles y valoraciones.
3. Publica una solicitud de servicio.
4. Los técnicos envían cotizaciones y el cliente elige una.

**Rationale:** Refleja el modelo de negocio completo aunque los pasos 3–4 no se implementen aún.

### 6. Filtrado funcional mínimo en búsqueda

**Decisión:** Array estático de técnicos simulados en `buscar-tecnicos.ts`. Filtros con `<select>` para categoría, zona y calificación mínima. Al cambiar un filtro, filtrar el array en memoria (método simple, sin backend).

**Alternativa descartada:** Filtros solo decorativos sin efecto en el listado.

**Rationale:** Demo creíble con complejidad mínima (~10–15 líneas de lógica).

### 7. Login/registro: una pantalla con pestañas y roles

**Decisión:** Una sola pantalla con:

- Pestañas visuales: **Iniciar sesión** | **Crear cuenta**
- Selector de rol: **Cliente** | **Técnico**
- Un formulario reutilizado cuyos campos/etiquetas cambian según pestaña y rol
- Formularios visuales sin submit funcional (`type="button"` o submit bloqueado)
- Sin opción de administrador

**Alternativa descartada:** Pantallas o rutas separadas para login y registro.

**Rationale:** UX clara y código simple para evaluación académica.

### 8. Estilos por componente

**Decisión:** Crear/completar `.css` en cada componente. Reutilizar variables de `styles.css`.

**Rationale:** Consistencia con el sprint de layout.

## Risks / Trade-offs

| Riesgo | Mitigación |
|--------|------------|
| Perfil siempre muestra el mismo técnico | Aceptable en prototipo; usar mismo técnico destacado que primera tarjeta del listado |
| Pasos 3–4 de la home no implementados aún | Texto informativo; sprint futuro implementa solicitud y cotizaciones |
| Botón solicitar servicio solo navega a login | Coherente con "sin auth real"; texto auxiliar explica el siguiente paso |
| Duplicación de datos mock entre búsqueda y perfil | Datos mínimos; perfil alineado narrativamente con listado |
| CSS faltante en componentes | Crear archivos `.css` en este sprint |

## Migration Plan

Cambio aditivo en componentes existentes. Verificación:

1. `npm run build` sin errores.
2. Navegar flujo: inicio → buscar (probar filtros) → perfil → login.
3. Confirmar CTA "Solicitar servicio" → `/login` con texto auxiliar.
4. Confirmar pestañas y roles en login; sin administrador.
5. Confirmar responsive en ~375px.

## Open Questions

- _(ninguna — decisiones cerradas antes de implementación)_
