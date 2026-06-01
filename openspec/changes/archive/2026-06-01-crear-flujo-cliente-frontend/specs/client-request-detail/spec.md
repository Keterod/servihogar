## ADDED Requirements

### Requirement: Request detail display

The request detail screen SHALL display complete information for a simulated service request.

#### Scenario: Request information visible

- **WHEN** the user navigates to `/detalle-solicitud`
- **THEN** the page displays category, description, status, tentative date, zone, and address

### Requirement: Quotations display

The request detail screen SHALL display three simulated quotations from different technicians.

#### Scenario: Quotations list visible

- **WHEN** the user views the quotations section
- **THEN** the page displays at least three quotations

#### Scenario: Each quotation shows key information

- **WHEN** the user views a quotation
- **THEN** the quotation displays technician name, specialty, rating, estimated price, estimated time, proposal details, and status

### Requirement: Quotation selection with signals

The request detail screen SHALL use Angular Signals to represent the selected or accepted quotation.

#### Scenario: Quotation selection signal

- **WHEN** the user views the quotations list
- **THEN** the selected quotation is stored in an Angular Signal

#### Scenario: Accept quotation button

- **WHEN** the user clicks "Aceptar" on a quotation
- **THEN** the quotation Signal updates to reflect the accepted quotation
- **THEN** the accepted quotation displays a visual "Aceptada" state
- **THEN** the other quotations display a "Rechazada" state or become visually disabled
- **THEN** a confirmation message is displayed
- **THEN** the request status changes to "en_proceso"

#### Scenario: Reject quotation button

- **WHEN** the user clicks "Rechazar" on a quotation
- **THEN** the quotation is visually marked as "Rechazada"
- **THEN** no HTTP request is made to the backend

#### Scenario: Buttons disabled after acceptance

- **WHEN** a quotation has been accepted
- **THEN** the accept/reject buttons of other quotations are disabled

### Requirement: Request detail navigation

The request detail screen SHALL be accessible from the client dashboard.

#### Scenario: Route accessible

- **WHEN** the user navigates to `/detalle-solicitud`
- **THEN** the request detail screen is displayed within the application layout

#### Scenario: Navigation to rating

- **WHEN** the user clicks a test button or the service is marked as completed
- **THEN** the application navigates to `/valorar-servicio` without a full page reload
