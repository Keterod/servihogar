# ServiHogar

Plataforma web académica para conectar clientes con técnicos independientes de servicios domésticos menores. El prototipo actual permite publicar solicitudes de servicio, buscar técnicos, recibir cotizaciones simuladas y valorar servicios finalizados, todo desde una interfaz funcional en el navegador.

---

## Estado actual del proyecto

| Aspecto           | Estado                                                  |
| ----------------- | ------------------------------------------------------- |
| **Frontend**      | Implementado (Angular 21)                               |
| **Backend**       | Planificado; **no integrado** todavía                   |
| **Base de datos** | PostgreSQL diseñada; **no conectada** al frontend       |
| **Autenticación** | **No implementada** (login/registro solo visual)        |
| **Datos**         | Simulados / mocks en memoria                            |
| **Paneles**       | Accesibles por rutas directas o enlaces demo del footer |

> **Importante:** el proyecto actual es un **prototipo frontend funcional con datos simulados**. No persiste información ni se comunica con un servidor real.

---

## Tecnologías usadas

| Área                  | Tecnología               | Notas                                          |
| --------------------- | ------------------------ | ---------------------------------------------- |
| Frontend              | **Angular 21**           | Aplicación principal                           |
| Lenguaje              | **TypeScript**           | Tipado estático                                |
| Estilos               | **CSS**                  | Sin librerías UI externas                      |
| Estado local          | **Angular Signals**      | Formularios, filtros, listas y datos derivados |
| Base de datos         | **PostgreSQL**           | Modelo diseñado / planificado                  |
| Backend               | **FastAPI** (Python)     | Planificado; carpeta preparada                 |
| Control de versiones  | **Git** y **GitHub**     | Repositorio remoto                             |
| Especificaciones      | **OpenSpec**             | Specs y cambios del proyecto                   |
| Herramientas de apoyo | **Cursor**, **OpenCode** | Desarrollo asistido y flujo spec-driven        |

---

## Requisitos previos (PC nueva)

Instala lo siguiente antes de clonar el proyecto:

| Herramienta                               | Propósito                                 |
| ----------------------------------------- | ----------------------------------------- |
| **Git**                                   | Clonar y versionar el repositorio         |
| **Node.js LTS**                           | Entorno de ejecución para Angular         |
| **npm**                                   | Gestor de paquetes (incluido con Node.js) |
| **Angular CLI**                           | Servidor de desarrollo y comandos `ng`    |
| **Visual Studio Code**                    | Editor recomendado                        |
| **PostgreSQL** + **pgAdmin** _(opcional)_ | Para la futura capa de base de datos      |

### Verificar instalación

```bash
git --version
node -v
npm -v
ng version
```

Si Angular CLI no está instalado:

```bash
npm install -g @angular/cli
```

---

## Cómo clonar el proyecto

```bash
git clone https://github.com/Keterod/servihogar.git
cd servihogar
```

---

## Cómo instalar dependencias del frontend

```bash
cd servihogar-frontend
npm install
```

---

## Cómo ejecutar el frontend

Desde la carpeta `servihogar-frontend/`:

```bash
ng serve
```

El puerto 4200 está ocupado

Ejecuta Angular en otro puerto:

```bash
ng serve --port 4300
```

También puedes usar:

```bash
npm start
```

Abre el navegador en:

**http://localhost:4200**

---

## Rutas disponibles para probar

| Ruta                   | Descripción                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| `/inicio`              | Página principal                                                  |
| `/buscar-tecnicos`     | Búsqueda de técnicos con filtros simulados                        |
| `/perfil-tecnico`      | Perfil público de técnico                                         |
| `/login`               | Pantalla visual de inicio de sesión y registro                    |
| `/solicitud-servicio`  | Formulario visual para publicar solicitud                         |
| `/panel-cliente`       | Panel del cliente con solicitudes simuladas                       |
| `/detalle-solicitud`   | Detalle de solicitud y cotizaciones                               |
| `/valorar-servicio`    | Valoración visual del servicio finalizado                         |
| `/panel-tecnico`       | Panel del técnico con solicitudes y cotizaciones                  |
| `/panel-administrador` | Panel administrador con técnicos, categorías, usuarios y reportes |

Algunas rutas internas también están accesibles desde el **footer**, en la sección **«Acceso demo (prototipo académico)»** (Panel cliente, Panel técnico, Panel administrador).

---

## Botones y acciones del prototipo

- Los **enlaces de navegación** del navbar y footer funcionan con el router de Angular.
- Varias **acciones modifican estado local** con Angular Signals (filtros, formularios, aceptar/rechazar cotizaciones, etc.).
- **No se guarda información** en base de datos; los cambios viven solo en memoria del navegador.
- **Login y registro son solo visuales**: no autentican usuarios ni validan credenciales.
- Acciones como **aceptar cotización**, **rechazar**, **valorar servicio**, **validar técnico** o **agregar categoría** operan sobre datos simulados y se pierden al recargar la página.

---

## Estructura del repositorio

```
ServiHogar/
├── servihogar-frontend/
├── servihogar-backend/
├── database/
├── docs/
├── openspec/
├── README.md
└── .gitignore
```

| Carpeta                | Descripción                                        |
| ---------------------- | -------------------------------------------------- |
| `servihogar-frontend/` | Aplicación Angular del prototipo                   |
| `servihogar-backend/`  | Backend planificado con FastAPI                    |
| `database/`            | Scripts y documentación de base de datos           |
| `docs/`                | Informe, diagramas y evidencias del proyecto       |
| `openspec/`            | Especificaciones y cambios del proyecto (OpenSpec) |

---

## Estructura principal del frontend

```
servihogar-frontend/src/app/
├── components/
├── models/
├── services/
├── app.routes.ts
├── app.config.ts
├── app.html
├── app.css
└── app.ts
```

| Carpeta / archivo | Descripción                                                         |
| ----------------- | ------------------------------------------------------------------- |
| `components/`     | Pantallas y componentes visuales (home, paneles, formularios, etc.) |
| `models/`         | Interfaces TypeScript del dominio                                   |
| `services/`       | Servicios base preparados para futura conexión con backend          |
| `app.routes.ts`   | Definición de rutas de la aplicación                                |
| `app.config.ts`   | Configuración global (router, scroll, etc.)                         |

---

## Uso de Angular Signals

El frontend usa **Angular Signals** para manejar estado local en componentes con formularios, filtros, listas simuladas y datos derivados (`computed()`).

Ejemplos en el proyecto:

| Pantalla              | Uso de Signals                                                       |
| --------------------- | -------------------------------------------------------------------- |
| `buscar-tecnicos`     | Filtros de categoría, zona y calificación; lista filtrada derivada   |
| `solicitud-servicio`  | Campos del formulario y validación antes de enviar                   |
| `detalle-solicitud`   | Cotizaciones, selección y aceptación/rechazo                         |
| `valorar-servicio`    | Calificaciones por criterio y promedio calculado                     |
| `panel-tecnico`       | Solicitudes disponibles, formulario de cotización y contadores       |
| `panel-administrador` | Validación de técnicos, categorías y métricas del panel              |
| `login-register`      | Pestaña activa (login/registro) y rol seleccionado (cliente/técnico) |

Los textos completamente estáticos (por ejemplo, contenido fijo de la home o perfil de referencia) no requieren Signals.

---

## Comandos útiles

### Frontend (`servihogar-frontend/`)

```bash
npm install
ng serve
npm run build
```

### Git (desde la raíz del repositorio)

```bash
git status
git branch
git checkout -b nombre-rama
git add .
git commit -m "mensaje"
git push origin nombre-rama
```

---

## Flujo de trabajo con ramas

- La rama **`main`** contiene los avances estables del proyecto.
- Cada nueva funcionalidad debe desarrollarse en una rama **`feature/nombre-descriptivo`**.
- Al terminar y verificar el cambio, se integra en `main` mediante merge o pull request.

---

## Limitaciones actuales

- No hay backend conectado.
- No hay autenticación real.
- No hay persistencia en base de datos.
- Los datos se reinician al recargar la página.
- Algunas acciones son solo visuales del prototipo académico.
- Los paneles no están protegidos por login todavía.

---

## Base de datos

- Se eligió **PostgreSQL** como motor relacional.
- El modelo físico, scripts y documentación están (o estarán) en la carpeta `database/`.
- La conexión real entre backend, base de datos y frontend se implementará en una fase posterior del proyecto.

---

## Autor

Desarrollado por **Diego Carhuamaca** como proyecto académico.
