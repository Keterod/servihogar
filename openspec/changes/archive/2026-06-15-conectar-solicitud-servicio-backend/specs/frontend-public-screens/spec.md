## MODIFIED Requirements

### Requirement: Technician profile page

The technician profile page SHALL display the selected technician's data fetched from `GET /tecnicos/{id}` including name, description, experience, rating, categories, zones, and portfolio images, with a single call-to-action to request service that navigates to `/solicitud-servicio` with the technician's ID and name as query params.

#### Scenario: Request service navigates to solicitud-servicio with query params

- **WHEN** the user clicks the "Solicitar cotización" button on the profile page
- **THEN** the application navigates to `/solicitud-servicio?tecnicoId={id}&tecnicoNombre={name}` without a full page reload
- **THEN** `tecnicoId` is the numeric ID of the displayed technician
- **THEN** `tecnicoNombre` is the full name (nombres + apellidos) of the displayed technician
