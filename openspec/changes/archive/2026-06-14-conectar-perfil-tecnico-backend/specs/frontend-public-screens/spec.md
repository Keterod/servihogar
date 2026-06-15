## MODIFIED Requirements

### Requirement: Technician profile page

The technician profile page SHALL display the selected technician's data fetched from `GET /tecnicos/{id}` including name, description, experience, rating, categories, zones, and portfolio images, with a single call-to-action to request service that navigates to login.

#### Scenario: Profile loaded from backend by ID

- **WHEN** the user navigates to `/perfil-tecnico/1`
- **THEN** the page fetches technician data from `GET /tecnicos/1`
- **THEN** the page displays the technician's full name, description, experience, rating, categories, zones, and portfolio images

#### Scenario: Loading state displayed

- **WHEN** the user navigates to `/perfil-tecnico/:id` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message

#### Scenario: Error state displayed when backend is unavailable

- **WHEN** the backend is unreachable or returns an error for `/tecnicos/:id`
- **THEN** the page SHALL display an error message indicating the backend is unavailable

#### Scenario: Not-found state for invalid ID

- **WHEN** the backend returns 404 for `/tecnicos/:id`
- **THEN** the page SHALL display a "Técnico no encontrado" message

#### Scenario: Request service navigates to login

- **WHEN** the user clicks the "Solicitar servicio" button on the profile page
- **THEN** the application navigates to `/login` without a full page reload

#### Scenario: Navigation from search results passes ID

- **WHEN** the user clicks "Ver perfil" on a technician card in `/buscar-tecnicos`
- **THEN** the application navigates to `/perfil-tecnico/{id_tecnico}` without a full page reload
