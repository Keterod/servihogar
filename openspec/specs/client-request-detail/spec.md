# client-request-detail Specification

## Purpose

Provides the request detail screen showing a service request and quotations from technicians, fetched from the backend.
## Requirements
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

The request detail screen SHALL use Angular Signals to represent the selected or accepted quotation based on backend data and SHALL persist accept/reject actions via the backend.

#### Scenario: Quotation selection signal

- **WHEN** the user views the quotations list loaded from the backend
- **THEN** the selected quotation is stored in an Angular Signal

#### Scenario: Accept quotation button

- **WHEN** the user clicks "Aceptar" on a pending quotation
- **THEN** the application SHALL PATCH `/cotizaciones/{id_cotizacion}/aceptar`
- **THEN** on HTTP 200 the cotizaciones Signal SHALL reflect the accepted and rejected states from the backend
- **THEN** the solicitud estado Signal SHALL update to `en_proceso` when returned by the backend
- **THEN** a confirmation message is displayed
- **THEN** accept/reject actions on other quotations are disabled as appropriate

#### Scenario: Accept loading state

- **WHEN** the user clicks "Aceptar" and the PATCH request is in flight
- **THEN** the accept/reject buttons for that quotation SHALL be disabled
- **THEN** a loading indication SHALL be visible

#### Scenario: Accept error state

- **WHEN** the backend returns an error other than success for accept
- **THEN** the page SHALL display a clear error message
- **THEN** local cotización and solicitud states SHALL NOT be incorrectly marked as accepted

#### Scenario: Reject quotation button

- **WHEN** the user clicks "Rechazar" on a pending quotation
- **THEN** the application SHALL PATCH `/cotizaciones/{id_cotizacion}/rechazar`
- **THEN** on HTTP 200 the quotation SHALL display estado `rechazada` from the backend response

#### Scenario: Reject loading state

- **WHEN** the user clicks "Rechazar" and the PATCH request is in flight
- **THEN** the reject button for that quotation SHALL be disabled
- **THEN** a loading indication SHALL be visible

#### Scenario: Reject error state

- **WHEN** the backend returns an error for reject
- **THEN** the page SHALL display a clear error message
- **THEN** the quotation SHALL retain its previous estado until a successful response

#### Scenario: Buttons disabled after acceptance

- **WHEN** a quotation has been accepted (from backend data or successful accept action)
- **THEN** the accept/reject buttons of other quotations are disabled
- **THEN** the accepted quotation cannot be rejected

#### Scenario: Persisted state after reload

- **WHEN** the user accepts or rejects a quotation and reloads `/detalle-solicitud/:id`
- **THEN** cotización estados and solicitud estado SHALL match the backend response from `GET /solicitudes/{id}`

### Requirement: Request detail navigation

The request detail screen SHALL be accessible from the client dashboard with the solicitud id in the route.

#### Scenario: Route accessible with id

- **WHEN** the user navigates to `/detalle-solicitud/:id`
- **THEN** the request detail screen is displayed within the application layout
- **THEN** the displayed solicitud matches the id in the URL

#### Scenario: Navigation to rating

- **WHEN** the user clicks a test button or the service is marked as completed
- **THEN** the application navigates to `/valorar-servicio` without a full page reload

