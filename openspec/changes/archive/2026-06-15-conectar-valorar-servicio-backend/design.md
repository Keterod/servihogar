## Context

- Client flow is connected end-to-end through accept/reject cotizaciones; accepted solicitudes use `estado = en_proceso`.
- `/valorar-servicio` is a prototype: mock technician/service data, local-only submit, five star criteria + optional comment.
- DB table `valoraciones` (unchanged):
  - `id_valoracion`, `id_cotizacion` (unique FK), `puntuacion` (1–5), `comentario`, optional `puntualidad`, `calidad`, `precio`, `trato`, `fecha_valoracion`
  - One valoración per cotización (unique on `id_cotizacion`)
- Solicitud states: `pendiente`, `en_proceso`, `finalizada`, `cancelada`
- Architecture: `main → apis → services → repository`; Supabase via service role only; demo client via `SolicitudesRepository.get_demo_cliente_id()`.

## Goals / Non-Goals

**Goals:**
- Persist client ratings via `POST /valoraciones` for the demo client
- Resolve `id_cotizacion` from the accepted cotización on the solicitud
- Validate ownership, accepted cotización, rating range, and duplicate prevention
- Set solicitud `estado = finalizada` after successful rating when currently `en_proceso`
- Wire `/valorar-servicio?idSolicitud=...` with real submit and UX states
- Link from `/detalle-solicitud/:id` when solicitud is `en_proceso` or `finalizada`

**Non-Goals:**
- Real authentication or multi-client authorization
- Editing or deleting valoraciones
- Technician notifications or live dashboard refresh
- Schema/seed migrations
- Persisting UI-only fields without DB columns (e.g. "limpieza", "volvería a contratar") unless stored in `comentario`

## Decisions

### 1. POST body uses `id_solicitud` + `calificacion`

**Choice:** Request fields: `id_solicitud`, `calificacion` (1–5), optional `comentario`. Optional sub-scores: `puntualidad`, `calidad`, `trato`, `precio` (each 1–5) mapped to DB columns when provided.

**Rationale:** Matches user requirement; backend resolves `id_cotizacion` from accepted cotización. Sub-scores reuse existing UI criteria without schema changes.

**Alternative:** Require `id_cotizacion` in request — rejected; client UI knows solicitud id, not cotización id.

### 2. Map frontend overall rating to `puntuacion`

**Choice:** `calificacion` in request maps to DB column `puntuacion`. Frontend may send rounded average of star criteria as `calificacion` and pass matching sub-scores when available.

**Rationale:** `puntuacion` is the required overall score in schema; sub-columns are optional detail.

**Note:** UI criterion "Limpieza" has no DB column; it contributes to computed average only (or maps to `calidad` if all five criteria are filled — implementation may send `calificacion` as average and map puntualidad/calidad/trato/precio from the four DB-aligned criteria).

### 3. Eligible solicitud states for rating

**Choice:** Allow rating when solicitud `estado` is `en_proceso` or `finalizada`, solicitud belongs to demo client, and accepted cotización exists.

**Rationale:** Client may rate after work completes (`en_proceso`); `finalizada` allows idempotent error (409 duplicate) if already rated.

**Reject** when `pendiente`, `cancelada`, or no accepted cotización → 400.

### 4. Finalize solicitud on successful rating

**Choice:** After insert, if solicitud is `en_proceso`, update to `finalizada`.

**Rationale:** Rating marks service completion in the demo flow; aligns with seed data pattern (finalizada solicitud + valoración).

### 5. Duplicate prevention

**Choice:** Check existing valoración by `id_cotizacion` before insert; rely on DB unique constraint as safety net → HTTP 409.

**Rationale:** `valoraciones.id_cotizacion` is unique; one rating per accepted cotización.

### 6. Response shape: `ValoracionResponse`

**Choice:** Return `id_valoracion`, `id_cotizacion`, `id_solicitud`, `puntuacion`, `comentario`, optional sub-scores, `fecha_valoracion`, `solicitud_estado` (post-update).

**Rationale:** Frontend can show confirmation and navigate without extra GET.

### 7. Frontend navigation and context

**Choice:** Route `/valorar-servicio?idSolicitud={id}`; load detail via existing `GET /solicitudes/{id}` to show solicitud #, accepted technician name, category/title.

**Alternative:** Path param `/valorar-servicio/:id` — rejected to minimize route changes; query param matches user requirement.

### 8. Error mapping

| Condition | HTTP |
|-----------|------|
| Solicitud not found or not owned by demo client | 404 |
| No accepted cotización on solicitud | 400 |
| Solicitud not eligible (`pendiente`, `cancelada`) | 400 |
| Calificación out of range | 422 |
| Valoración already exists for cotización | 409 |
| Supabase failure | 503 |

## Risks / Trade-offs

- **[UI vs DB columns] Five criteria vs four optional DB columns** → Mitigation: send overall `calificacion` as `puntuacion`; map four aligned criteria to DB; limpieza affects average only
- **[Rating before work done] Client rates while still en_proceso** → Mitigation: acceptable for demo; detail screen only shows rating link when eligible
- **[Stale panel after rating]** → Mitigation: panel refetches on navigation; no websockets
- **[409 on reload]** → Mitigation: frontend shows duplicate message and offers navigation back

## Migration Plan

1. Deploy backend with `POST /valoraciones` (backward compatible).
2. Deploy frontend wired to POST and detail navigation.
3. Verify: accept cotización → open valorar → submit → solicitud `finalizada`, duplicate blocked.
4. Rollback: revert frontend to simulated submit; backend route unused harmlessly.

## Open Questions

- None blocking — use query param `idSolicitud` and finalize solicitud on first successful rating.
