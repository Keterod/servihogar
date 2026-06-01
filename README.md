# ServiHogar

Plataforma para conectar clientes con técnicos de servicios del hogar: búsqueda de profesionales, solicitudes de servicio, cotizaciones y valoraciones.

## Tecnologías

| Área | Stack |
|------|-------|
| **Frontend** | Angular 21, TypeScript, CSS |
| **Backend** | Python, FastAPI |
| **Base de datos** | PostgreSQL |
| **Metodología** | Spec Driven Development con [OpenSpec](openspec/) |

## Estructura del repositorio

```
ServiHogar/
├── servihogar-frontend/   # Aplicación web (Angular 21)
├── servihogar-backend/    # API REST (Python + FastAPI)
├── database/              # Scripts SQL, modelo físico y documentación de BD
├── docs/                  # Informe, diagramas y evidencias del proyecto
├── openspec/              # Especificaciones y cambios (OpenSpec)
├── .cursor/               # Configuración de Cursor IDE
└── .opencode/             # Configuración de OpenCode
```

## Comandos básicos

### Frontend

```bash
cd servihogar-frontend
npm install
ng serve
```

La aplicación quedará disponible en `http://localhost:4200`.

### Backend

Consulta el README dentro de `servihogar-backend/` cuando el entorno esté configurado.
