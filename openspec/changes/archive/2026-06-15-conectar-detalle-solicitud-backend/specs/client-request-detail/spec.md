## MODIFIED Requirements

### Requirement: Request detail display

The request detail screen SHALL fetch and display complete information for the service request identified by the route parameter `:id` from `GET /solicitudes/{id_solicitud}`.

#### Scenario: Request information visible

- **WHEN** the user navigates to `/detalle-solicitud/9`
- **THEN** the page fetches data from `GET /solicitudes/9`
- **THEN** the page displays the real solicitud number, category, description, status, publication date, zone, and address from the backend response

#### Scenario: Loading state

- **WHEN** the user navigates to `/detalle-solicitud/:id` and data is being fetched
- **THEN** the page displays a loading indicator

#### Scenario: Error state

- **WHEN** the backend is unreachable or returns a server error
- **THEN** the page displays an error message
- **THEN** the user can navigate back to the panel

#### Scenario: Not found state

- **WHEN** the backend returns HTTP 404 for the solicitud id
- **THEN** the page displays a not-found message

### Requirement: Quotations display

The request detail screen SHALL display cotizaciones returned by the backend for the selected solicitud.

#### Scenario: Quotations list visible when data exists

- **WHEN** the user views a solicitud that has cotizaciones in the backend response
- **THEN** the page displays each cotización with technician name, specialty/description, price, estimated time, proposal description, and status

#### Scenario: Empty quotations state

- **WHEN** the backend returns an empty `cotizaciones` array
- **THEN** the page displays the message "Aún no hay cotizaciones para esta solicitud."
- **THEN** the page SHALL NOT display simulated cotizaciones

#### Scenario: Each quotation shows key information

- **WHEN** the user views a quotation from the backend
- **THEN** the quotation displays technician name, price, estimated time, proposal details, and status from the API response

### Requirement: Quotation selection with signals

The request detail screen SHALL use Angular Signals to represent the selected or accepted quotation based on backend data.

#### Scenario: Quotation selection signal

- **WHEN** the user views the quotations list loaded from the backend
- **THEN** the selected quotation is stored in an Angular Signal

#### Scenario: Accept quotation button

- **WHEN** the user clicks "Aceptar" on a quotation
- **THEN** the quotation Signal updates to reflect the accepted quotation locally
- **THEN** the accepted quotation displays a visual "Aceptada" state
- **THEN** the other quotations display a "Rechazada" state or become visually disabled
- **THEN** a confirmation message is displayed
- **THEN** no HTTP request is made to the backend in this phase

#### Scenario: Reject quotation button

- **WHEN** the user clicks "Rechazar" on a quotation
- **THEN** the quotation is visually marked as "Rechazada" locally
- **THEN** no HTTP request is made to the backend

#### Scenario: Buttons disabled after acceptance

- **WHEN** a quotation has been accepted locally
- **THEN** the accept/reject buttons of other quotations are disabled

### Requirement: Request detail navigation

The request detail screen SHALL be accessible from the client dashboard with the solicitud id in the route.

#### Scenario: Route accessible with id

- **WHEN** the user navigates to `/detalle-solicitud/:id`
- **THEN** the request detail screen is displayed within the application layout
- **THEN** the displayed solicitud matches the id in the URL

#### Scenario: Navigation to rating

- **WHEN** the user clicks a test button or the service is marked as completed
- **THEN** the application navigates to `/valorar-servicio` without a full page reload

## REMOVED Requirements

### Requirement: Request detail display

**Reason**: Replaced by backend-fetched solicitud detail via `GET /solicitudes/{id_solicitud}`

**Migration**: The page no longer uses hardcoded mock solicitud #1 data

#### Scenario: Request information visible

**Reason**: Superseded by backend-backed scenario with route param `:id`

**Migration**: Fetch from `GET /solicitudes/{id_solicitud}` on load

### Requirement: Quotations display

**Reason**: Replaced by real cotizaciones from the backend; empty array shows empty state instead of mock data

**Migration**: Remove hardcoded cotizaciones array from the component

#### Scenario: Quotations list visible

**Reason**: Replaced by conditional display based on backend response length

**Migration**: Show list when `cotizaciones.length > 0`, otherwise empty state message

#### Scenario: Each quotation shows key information

**Reason**: Data source changed from mock to API fields

**Migration**: Bind template to `CotizacionDetalleResponse` interface fields
