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

#### Scenario: Visual cotización action without backend submit

- **WHEN** the user clicks "Enviar cotización" on an available request
- **THEN** the UI SHALL present the quotation form or equivalent visual flow
- **THEN** no HTTP POST request for cotización SHALL be made

### Requirement: Signals and computed values

The technician dashboard SHALL use Angular Signals for local state and computed() for derived values.

#### Scenario: Core signals defined

- **WHEN** the technician dashboard loads
- **THEN** tecnico, solicitudesDisponibles, cotizacionesEnviadas, serviciosAceptados, solicitudSeleccionada, formCotizacion, estadoValidacion, cargando, and error are managed with Signals

#### Scenario: Computed summary and validation

- **WHEN** the user views the dashboard
- **THEN** counts for available requests, pending-to-quote requests, and already-quoted available requests are computed from the backend-fetched solicitudesDisponibles Signal
- **THEN** counts for sent quotations and accepted services remain computed from their respective Signals
- **THEN** puedeEnviarCotizacion is computed from form validity, selected request, and validation status

## REMOVED Requirements

### Requirement: Only gasfitería requests available

**Reason**: Available requests are now determined by backend filtering on the demo technician's full category list (Gasfitería menor and Electricidad básica), not a hardcoded gasfitería-only mock filter.

**Migration**: Expect backend to return any category assigned to Carlos Mendoza that matches a pending solicitud.

### Requirement: Already quoted request excluded

**Reason**: Backend returns pending solicitudes with `ya_cotizada_por_tecnico` flag instead of hiding them; UI distinguishes quoted vs not-yet-quoted via computed counts.

**Migration**: Use `ya_cotizada_por_tecnico` and summary computed values instead of removing solicitudes from the list.

### Requirement: Available request IDs

**Reason**: Available request ids are dynamic from Supabase, not hardcoded mock ids 2 and 3.

**Migration**: Verify against real seed and POST-created solicitudes matching Carlos Mendoza's categories and zones.
