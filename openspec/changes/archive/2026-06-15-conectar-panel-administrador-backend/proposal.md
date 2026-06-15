## Why

El `/panel-administrador` todavía depende de datos quemados, mientras el resto de flujos principales ya consulta FastAPI y Supabase. Esta desconexión impide que el administrador demo vea el estado real del sistema y gestione técnicos pendientes creados en la base de datos.

## What Changes

### Backend
- **New endpoints** under `/admin/demo` for the administrator demo panel:
  - `GET /admin/demo/resumen`
  - `GET /admin/demo/tecnicos-pendientes`
  - `PATCH /admin/demo/tecnicos/{id_tecnico}/aprobar`
  - `PATCH /admin/demo/tecnicos/{id_tecnico}/rechazar`
- **Real metrics** calculated from Supabase: users, clients, technicians, service requests by state, technician validation states, quotations, and ratings.
- **Technician validation workflow** that validates technician existence and changes `estado_validacion` to `validado` or `rechazado` with controlled error handling for invalid/current states.

### Frontend
- **PanelAdministrador connection:** replace hardcoded dashboard metrics and pending technician data with backend responses.
- **Service addition:** create or adapt an Angular service that consumes the new `/admin/demo` endpoints through FastAPI only.
- **Pending technician management:** show real pending technicians with contact, description, experience, categories, zones, and approve/reject actions.
- **UI states:** loading, error, empty, success, and loaded states for the administrator panel.
- **Reactive state:** use Angular Signals and `computed()` for panel state and derived values.

## Capabilities

### New Capabilities
- `admin-demo-api`: Backend demo administrator API for dashboard summary metrics, pending technician listing, and technician approval/rejection actions.

### Modified Capabilities
- `admin-dashboard`: Replace simulated administrator data with backend-fetched metrics and pending technician management while keeping Angular Signals and existing route behavior.

## Impact

- **Backend:** New admin API router, service, repository methods, and Pydantic schemas following `main -> apis -> services -> repository`.
- **Frontend:** Updated `/panel-administrador` component, admin-facing service/model additions, and real loading/error/empty/success behavior.
- **Supabase:** Reads existing tables and updates technician validation state only; no schema or seed changes.
- **No auth:** Uses demo administrator endpoints until real authentication is introduced.
- **No direct Supabase in Angular:** Frontend communicates only with FastAPI.
- **Regression scope:** Must preserve `/buscar-tecnicos`, `/panel-cliente`, `/panel-tecnico`, and `/detalle-solicitud/:id`.
