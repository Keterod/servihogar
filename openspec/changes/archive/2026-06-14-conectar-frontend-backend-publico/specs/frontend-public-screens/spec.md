## MODIFIED Requirements

### Requirement: Technician search page

The search page SHALL display filters for category (populated from the backend), zone (populated from the backend), and minimum rating, and a list of technicians fetched from the backend `GET /tecnicos` endpoint, filtered accordingly.

#### Scenario: Filters populated from backend categories and zones

- **WHEN** the user navigates to `/buscar-tecnicos`
- **THEN** the category filter options SHALL be fetched from `GET /categorias`
- **THEN** the zone filter options SHALL be fetched from `GET /zonas`
- **THEN** the page displays at least three technician cards when the backend has seed data

#### Scenario: Filtering is client-side with Signals

- **WHEN** the user changes category, zone, or minimum rating filters
- **THEN** the displayed technician list updates using `computed()` and filtering is done client-side on the fetched data
- **THEN** no additional backend requests are made per filter change

#### Scenario: Loading state displayed

- **WHEN** the user navigates to `/buscar-tecnicos` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message

#### Scenario: Error state displayed

- **WHEN** the backend is unreachable or returns an error
- **THEN** the page SHALL display an error message indicating the backend is unavailable
- **THEN** filter dropdowns SHALL be empty

#### Scenario: Empty state displayed

- **WHEN** the backend returns zero technicians
- **THEN** the page SHALL display a "no technicians found" message (distinct from loading and error states)

### Requirement: Simulated data only

**Reason**: This requirement is superseded by the real backend connection. Technicians, categories, and zones are now fetched from the FastAPI backend instead of using static in-component data.

**Migration**: Components should use service methods from `tecnico.service.ts`, `categoria-servicio.service.ts`, and `zona.service.ts` instead of hardcoded arrays. The `BuscarTecnicos` component has been migrated. Other screens remain on mock data for now.
