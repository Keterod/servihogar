# frontend-image-upload Specification

## Purpose
TBD - created by archiving change implementar-evidencias-imagenes. Update Purpose after archive.
## Requirements
### Requirement: Storage upload service

The frontend SHALL provide a service that uploads image files to Supabase Storage bucket `servihogar-evidencias` using only the Supabase anon key and the authenticated user's session.

#### Scenario: Upload solicitud image

- **WHEN** a client selects a valid image after creating solicitud `id_solicitud=12`
- **THEN** the service SHALL upload to path `solicitudes/12/{timestamp}-{sanitizedFilename}`
- **THEN** the service SHALL return the storage path for backend metadata registration

#### Scenario: Upload portfolio image

- **WHEN** a validated technician selects a valid image
- **THEN** the service SHALL upload to path `tecnicos/{id_tecnico}/portafolio/{timestamp}-{sanitizedFilename}`

#### Scenario: Rejects invalid MIME type

- **WHEN** the user selects a file that is not JPEG, PNG, or WebP
- **THEN** the service SHALL reject before upload with a user-visible error

#### Scenario: Rejects oversized file

- **WHEN** the file size exceeds 5 MB
- **THEN** the service SHALL reject before upload with a user-visible error

#### Scenario: No service role in frontend

- **WHEN** inspecting frontend environment and services
- **THEN** the Supabase service role key SHALL NOT be present or used

### Requirement: Solicitud form image picker

The service request form SHALL allow selecting up to 5 optional images before or after submitting the solicitud, displaying previews and upload progress.

#### Scenario: Preview selected images

- **WHEN** the client selects 2 valid images on `/solicitud-servicio`
- **THEN** the UI SHALL show thumbnails and allow removing a selection before submit

#### Scenario: Upload after solicitud creation

- **WHEN** the client submits the form successfully and selected images exist
- **THEN** each image SHALL upload to Storage and register via `POST /solicitudes/{id}/imagenes` with Bearer token

#### Scenario: Solicitud succeeds without images

- **WHEN** the client submits without selecting images
- **THEN** the flow SHALL complete normally without image upload steps

### Requirement: Portfolio upload in technician panel

The technician panel SHALL include a section to view existing portfolio items and add new ones with titulo, optional descripcion, and one image.

#### Scenario: List own portfolio in panel

- **WHEN** a validated technician opens `/panel-tecnico`
- **THEN** the panel SHALL fetch `GET /tecnicos/me/portafolio` with Bearer token and display items

#### Scenario: Add portfolio item

- **WHEN** the technician fills titulo, selects an image, and submits
- **THEN** the image SHALL upload to Storage and metadata SHALL POST to `/tecnicos/me/portafolio`

### Requirement: Image gallery in request detail

The request detail screen SHALL display solicitud images from the `imagenes` field when present.

#### Scenario: Gallery visible with images

- **WHEN** `/detalle-solicitud/:id` loads and the API returns non-empty `imagenes`
- **THEN** the page SHALL render a gallery with alt text from descripcion or solicitud context

#### Scenario: No gallery when empty

- **WHEN** `imagenes` is empty
- **THEN** the gallery section SHALL be hidden or show a neutral empty state without breaking layout

