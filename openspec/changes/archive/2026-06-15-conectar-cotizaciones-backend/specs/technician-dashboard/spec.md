## MODIFIED Requirements

### Requirement: Available service requests as cards

The technician dashboard SHALL display available service requests fetched from `GET /tecnicos/demo/solicitudes-disponibles`, showing only pending requests matching the demo technician's categories and zones from the backend.

#### Scenario: Available requests loaded from backend

- **WHEN** the user navigates to `/panel-tecnico`
- **THEN** the page fetches available requests from `GET /tecnicos/demo/solicitudes-disponibles`
- **THEN** each request displays id, category name, description, zone name, publication date, approximate address, and estado

#### Scenario: Loading state for available requests

- **WHEN** the user navigates to `/panel-tecnico` and data is being fetched
- **THEN** the page SHALL show a loading indicator or message for the available requests section

#### Scenario: Error state for available requests

- **WHEN** the backend is unreachable or returns an error while loading available requests
- **THEN** the page SHALL display an error message indicating the backend is unavailable

#### Scenario: Empty state for available requests

- **WHEN** the backend returns an empty array of available requests
- **THEN** the page SHALL display a message indicating no solicitudes are available

#### Scenario: Finalized requests not shown

- **WHEN** the user views available service requests from the backend
- **THEN** solicitudes with estado finalizada SHALL NOT appear in the available list

#### Scenario: Navigate to request detail

- **WHEN** the user clicks "Ver detalle" on an available request
- **THEN** the application navigates to `/detalle-solicitud/{id_solicitud}` without a full page reload

#### Scenario: Cotización form opens from available request

- **WHEN** the user clicks "Enviar cotización" on an available request that is not yet quoted
- **THEN** the UI SHALL present the quotation form with precio, tiempo estimado, and propuesta fields

### Requirement: One quotation per request

The technician dashboard SHALL allow only one cotización per service request for the demo technician, enforced by the backend.

#### Scenario: Submit valid quotation to backend

- **WHEN** the user fills a valid quotation and submits while validated
- **THEN** the application SHALL POST to `/cotizaciones` with `id_solicitud`, `precio`, `tiempo_estimado`, and `descripcion_propuesta`
- **THEN** on HTTP 201 the solicitud SHALL be marked as already quoted in the available list
- **THEN** `cotizaciones_count` for that solicitud SHALL increase if displayed

#### Scenario: Submit loading state

- **WHEN** the user submits a quotation and the request is in flight
- **THEN** the submit button SHALL be disabled and a loading state SHALL be visible

#### Scenario: Submit success feedback

- **WHEN** the backend returns HTTP 201
- **THEN** the form SHALL reset and the solicitud selection SHALL clear
- **THEN** a success indication SHALL be shown to the user

#### Scenario: Duplicate quotation error

- **WHEN** the backend returns HTTP 409 because the technician already quoted the solicitud
- **THEN** the page SHALL display a clear error message
- **THEN** the solicitud SHALL remain marked as already quoted

#### Scenario: Submit error for other failures

- **WHEN** the backend is unreachable or returns an error other than 409
- **THEN** the page SHALL display an error message indicating the cotización could not be sent

#### Scenario: Quotation blocked when not validated

- **WHEN** the technician validation status is pendiente or rechazado
- **THEN** the submit quotation button SHALL be visually disabled

## REMOVED Requirements

### Requirement: Visual cotización action without backend submit

**Reason**: Cotizaciones are now persisted via `POST /cotizaciones`; the visual form submits to the backend.

**Migration**: Replace local-only submit with HTTP POST; handle 201/409/error responses in the panel.

### Requirement: No backend on submit

**Reason**: Superseded by backend-connected cotización creation under "One quotation per request".

**Migration**: Remove scenario from "Visual quotation form with signals"; submit now calls `POST /cotizaciones`.
