## MODIFIED Requirements

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
