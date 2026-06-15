## MODIFIED Requirements

### Requirement: Client dashboard display

The client dashboard SHALL display the demo client's service requests fetched from `GET /clientes/demo/solicitudes`.

#### Scenario: Requests list fetched from backend

- **WHEN** the user navigates to `/panel-cliente`
- **THEN** the page fetches requests from `GET /clientes/demo/solicitudes`
- **THEN** each request displays category name, description, zone name, tentative date, status, and number of quotations

#### Scenario: Loading state displayed

- **WHEN** the user navigates to `/panel-cliente` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message

#### Scenario: Error state displayed

- **WHEN** the backend is unreachable or returns an error
- **THEN** the page SHALL display an error message indicating the backend is unavailable

#### Scenario: Empty state displayed

- **WHEN** the demo client has no service requests
- **THEN** the page SHALL display a message indicating no requests found, with a link to create one

### Requirement: Dashboard navigation

#### Scenario: Select request navigates with ID

- **WHEN** the user clicks "Ver detalle" on a service request
- **THEN** the application navigates to `/detalle-solicitud/{id_solicitud}` without a full page reload
