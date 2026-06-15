## Why

The `/buscar-tecnicos` screen now fetches real technicians from the backend, but clicking "Ver perfil" still shows hardcoded mock data on `/perfil-tecnico`. The profile screen needs to display the selected technician's real data (categories, zones, portfolio) fetched from FastAPI, completing the public browse → view flow with real data.

## What Changes

### Backend
- **New endpoint** `GET /tecnicos/{id_tecnico}` returning detailed technician data

### Frontend
- **Route change:** `/perfil-tecnico` → `/perfil-tecnico/:id` with lazy loading
- **Navigation update:** "Ver perfil" link in `BuscarTecnicos` passes the technician's `id_tecnico`
- **Component rewrite:** `PerfilTecnico` reads route param, fetches from backend, uses Signals for loading/error states
- **Service addition:** `obtenerTecnicoPorId(id)` in `TecnicoService`
- **Model addition:** `TecnicoDetalle` interface with new backend fields (categorias, zonas, portafolio)
- **No auth** — remains public

## Capabilities

### New Capabilities
- `perfil-tecnico-backend`: FastAPI endpoint `GET /tecnicos/{id_tecnico}` returning detailed profile with categories, zones, and portfolio data from Supabase

### Modified Capabilities
- `frontend-api-connection`: Add scenario for `TecnicoService.obtenerTecnicoPorId` returning `Observable<TecnicoDetalle>` from `GET /tecnicos/{id_tecnico}`
- `frontend-public-screens`: Update "Technician profile page" requirement — replace simulated Carlos Mendoza data with real backend-fetched data, add loading/error/not-found states

## Impact

- **Backend:** New schema `TecnicoDetalleResponse`, new router in `src/apis/tecnicos.py`, new service/repo methods
- **Frontend:** Route param `:id`, `TecnicoDetalle` model, updated `TecnicoService`, full `PerfilTecnico` component rewrite
- **No DB schema changes** — uses existing `portafolio_tecnico` table via Supabase
