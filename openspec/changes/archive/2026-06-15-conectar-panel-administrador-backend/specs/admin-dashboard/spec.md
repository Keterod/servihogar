## MODIFIED Requirements

### Requirement: Admin dashboard summary
The admin dashboard SHALL display a general system summary grid with real metrics loaded from the FastAPI administrator demo API and local derived state managed with Signals and `computed()`.

#### Scenario: Real summary counters visible
- **WHEN** the user navigates to `/panel-administrador` and the summary request succeeds
- **THEN** the page displays counters for total users, clients, technicians, service requests, pending requests, in-process requests, finalized requests, pending technicians, validated technicians, rejected technicians, quotations, and ratings

#### Scenario: Counters come from backend response
- **WHEN** the admin dashboard renders summary counters
- **THEN** the displayed values are derived from `GET /admin/demo/resumen`
- **THEN** the counters are not initialized from hardcoded demo arrays

#### Scenario: Summary uses computed state
- **WHEN** the admin dashboard loads or technician validation changes
- **THEN** summary display state is derived using `computed()` from backend-loaded summary and UI state Signals

#### Scenario: Summary refreshes after validation action
- **WHEN** a pending technician is approved or rejected successfully
- **THEN** the dashboard reloads or updates the summary metrics so pending, validated, and rejected technician counters reflect the current backend state

### Requirement: Technician validation management
The admin dashboard SHALL display real pending technicians loaded from FastAPI and allow approving or rejecting pending technicians through backend actions only.

#### Scenario: Pending technician fields displayed
- **WHEN** the user views the pending technician list after data loads
- **THEN** each technician displays name, email when available, phone when available, description, experience years, categories, zones, and registration or creation date

#### Scenario: Only pending technicians are listed
- **WHEN** the admin dashboard displays the validation list
- **THEN** the list contains technicians returned by `GET /admin/demo/tecnicos-pendientes`
- **THEN** validated and rejected technicians are not shown in the pending list

#### Scenario: Approve pending technician
- **WHEN** the user clicks approve on a pending technician
- **THEN** the component shows an action loading state for that technician
- **THEN** the frontend calls `PATCH /admin/demo/tecnicos/{id_tecnico}/aprobar`
- **THEN** the technician is removed from the pending list after success
- **THEN** summary counters update reactively
- **THEN** a success message is displayed

#### Scenario: Reject pending technician
- **WHEN** the user clicks reject on a pending technician
- **THEN** the component shows an action loading state for that technician
- **THEN** the frontend calls `PATCH /admin/demo/tecnicos/{id_tecnico}/rechazar`
- **THEN** the technician is removed from the pending list after success
- **THEN** summary counters update reactively
- **THEN** a success message is displayed

#### Scenario: Action failure is controlled
- **WHEN** approving or rejecting a technician fails
- **THEN** the component clears the action loading state
- **THEN** an error message is displayed without removing the technician optimistically

### Requirement: Basic reports display
The admin dashboard SHALL display real system report metrics using values returned by the FastAPI administrator demo summary endpoint.

#### Scenario: Real report metrics visible
- **WHEN** the user views report or metric cards on `/panel-administrador`
- **THEN** the cards display real values for service requests, quotations, finalized services, active or validated technicians, and registered users from `GET /admin/demo/resumen`

#### Scenario: No fixed report values
- **WHEN** the admin dashboard renders report or metric values
- **THEN** solicitudes, cotizaciones, finalized services, technicians, and users are not displayed from fixed narrative constants

### Requirement: Single component layout with signals
The admin dashboard SHALL be implemented in the `panel-administrador` screen using Angular Signals for loaded backend data, UI state, and derived values.

#### Scenario: Single screen structure
- **WHEN** the user navigates to `/panel-administrador`
- **THEN** the connected administrator panel renders within the existing panel-administrador route without introducing eager-loaded page routes

#### Scenario: Core signals defined
- **WHEN** the admin dashboard loads
- **THEN** summary data, pending technicians, loading state, error state, action-in-progress state, and success message are managed with Signals

#### Scenario: Derived state uses computed
- **WHEN** the component determines whether to show loading, error, empty, or data content
- **THEN** it uses `computed()` for derived UI state where applicable

## ADDED Requirements

### Requirement: Admin dashboard API service
The frontend SHALL use an Angular service to communicate with the FastAPI administrator demo endpoints.

#### Scenario: Service exposes typed methods
- **WHEN** the admin dashboard needs data or actions
- **THEN** it uses typed service methods for `GET /admin/demo/resumen`, `GET /admin/demo/tecnicos-pendientes`, `PATCH /admin/demo/tecnicos/{id_tecnico}/aprobar`, and `PATCH /admin/demo/tecnicos/{id_tecnico}/rechazar`

#### Scenario: No direct Supabase usage
- **WHEN** `/panel-administrador` loads or performs technician validation actions
- **THEN** Angular communicates only with FastAPI and does not import or call Supabase directly

### Requirement: Admin dashboard loading, error, empty, and success states
The admin dashboard SHALL show controlled UI states while loading data, when data is unavailable, and after validation actions.

#### Scenario: Initial loading state
- **WHEN** `/panel-administrador` starts loading backend data
- **THEN** the page displays a loading state for the summary and pending technician sections

#### Scenario: Backend error state
- **WHEN** loading summary or pending technicians fails
- **THEN** the page displays a controlled error message instead of hardcoded fallback data

#### Scenario: Empty pending technician state
- **WHEN** the backend returns no pending technicians
- **THEN** the page displays an empty state indicating there are no technicians pending validation

#### Scenario: Loaded data state
- **WHEN** summary and pending technician requests succeed
- **THEN** the page displays backend-loaded metrics and the pending technician list or empty state

#### Scenario: Success state after validation
- **WHEN** a technician is approved or rejected successfully
- **THEN** the page displays a brief success message describing the completed action

### Requirement: Existing administrator route compatibility
The connected administrator dashboard SHALL preserve existing navigation behavior outside the administrator panel.

#### Scenario: Existing application routes are not broken
- **WHEN** the admin dashboard connection is implemented
- **THEN** `/buscar-tecnicos`, `/panel-cliente`, `/panel-tecnico`, and `/detalle-solicitud/:id` remain routable and keep their existing backend integrations

## REMOVED Requirements

### Requirement: Service category management
**Reason**: This change connects the administrator panel to real backend metrics and pending technician validation. Category creation remains out of scope because there is no requested administrator category API in this change.

**Migration**: Remove or de-emphasize hardcoded category management UI from `/panel-administrador`; future category administration should be specified with dedicated backend endpoints.

### Requirement: Registered users display
**Reason**: This change requires real aggregate user metrics, not a hardcoded list of five simulated users. No user listing endpoint is included in the requested scope.

**Migration**: Replace simulated registered-user list content with real summary counters from `GET /admin/demo/resumen`. A future change can add a paginated user management API if needed.
