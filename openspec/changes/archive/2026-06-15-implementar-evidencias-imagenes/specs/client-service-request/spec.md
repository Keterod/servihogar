## ADDED Requirements

### Requirement: Optional image attachments on service request

The service request form SHALL allow the authenticated client to attach up to 5 optional photos that are uploaded to Supabase Storage and registered via the backend after the solicitud is created.

#### Scenario: Image attachment control visible

- **WHEN** an authenticated client navigates to `/solicitud-servicio`
- **THEN** the form SHALL display a file input or drop zone accepting JPEG, PNG, and WebP up to 5 MB each
- **THEN** the control SHALL indicate a maximum of 5 images

#### Scenario: Images uploaded after successful submit

- **WHEN** the client submits a valid solicitud with 2 selected images
- **THEN** the application SHALL POST `/solicitudes` with Bearer token
- **THEN** after HTTP 201 the application SHALL upload both images and register metadata for the new `id_solicitud`

#### Scenario: Submit succeeds without images

- **WHEN** the client submits without selecting images
- **THEN** no Storage upload or image metadata calls SHALL occur
- **THEN** success feedback and navigation behave as today
