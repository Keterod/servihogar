## Context

- `GET /solicitudes/{id}` returns solicitud detail and cotizaciones for the demo client (Ana Torres).
- `POST /cotizaciones` lets the demo technician create real cotizaciones with `estado = pendiente`.
- `DetalleSolicitud` currently mutates Signals locally on accept/reject; `localEstadoOverride` simulates `en_proceso`.
- DB states (unchanged):
  - `solicitudes_servicio.estado`: `pendiente`, `en_proceso`, `finalizada`, `cancelada`
  - `cotizaciones.estado`: `pendiente`, `aceptada`, `rechazada`, `retirada`
  - Unique partial index: one `aceptada` cotización per solicitud
- Architecture: `main → apis → services → repository`; Supabase via service role only.

## Goals / Non-Goals

**Goals:**
- Persist accept/reject from `/detalle-solicitud/:id` via FastAPI
- On accept: one `aceptada` cotización, other pending cotizaciones on same solicitud → `rechazada`, solicitud → `en_proceso`
- On reject: target cotización → `rechazada`, solicitud unchanged if no accepted cotización exists
- Return updated cotización (and solicitud estado when applicable) to the frontend
- Wire Angular detail screen with loading/error UX; keep Signals/computed pattern

**Non-Goals:**
- Real authentication or multi-client authorization
- Notifications, messaging, or technician panel live updates (reload/refetch is enough)
- Valoración flow changes
- Schema/seed migrations
- Withdraw (`retirada`) cotizaciones

## Decisions

### 1. PATCH sub-resources on existing cotizaciones router

**Choice:** `PATCH /cotizaciones/{id_cotizacion}/aceptar` and `PATCH /cotizaciones/{id_cotizacion}/rechazar` on `apis/cotizaciones.py`.

**Rationale:** Keeps cotización lifecycle in one router; avoids a separate client-actions module. RESTful enough for demo scope.

**Alternative:** `POST /solicitudes/{id}/cotizaciones/{id}/aceptar` — rejected; cotización id is sufficient and already known in the UI.

### 2. Solicitud estado on accept → `en_proceso`

**Choice:** When a cotización is accepted, set `solicitudes_servicio.estado = 'en_proceso'`.

**Rationale:** Schema has no `aceptada` solicitud state; seed and frontend timeline already treat accepted quote + `en_proceso` as the post-acceptance phase.

### 3. Reject other pending cotizaciones on accept

**Choice:** In one service operation, set target to `aceptada`, bulk-update other `pendiente` cotizaciones on same `id_solicitud` to `rechazada`.

**Rationale:** Matches current local UI behavior and unique index constraint; avoids ambiguous multi-pending states after acceptance.

### 4. Demo client ownership check

**Choice:** Resolve demo `id_cliente` via existing `SolicitudesRepository.get_demo_cliente_id()`; verify cotización's solicitud belongs to that client before any mutation.

**Rationale:** Consistent with `GET /solicitudes/{id}`; returns 404 for unauthorized/not-found (no leak).

### 5. Response shape: `CotizacionActionResponse`

**Choice:** Response includes updated cotización fields plus `solicitud_estado` (and optionally `id_solicitud`) so the frontend can update Signals without a second GET.

**Fields:** `id_cotizacion`, `id_solicitud`, `estado`, `precio`, `descripcion_propuesta`, `tiempo_estimado`, `fecha_creacion`, `solicitud_estado`.

**Alternative:** Return full solicitud detail — rejected as heavier; detail screen already has solicitud context.

### 6. Frontend: optimistic vs refetch

**Choice:** On success, update local Signals from PATCH response; optionally refetch detail on error recovery. No optimistic UI before response.

**Rationale:** Simpler error handling; backend is source of truth for multi-cotización side effects on accept.

### 7. Error mapping

| Condition | HTTP |
|-----------|------|
| Cotización not found | 404 |
| Solicitud not owned by demo client | 404 |
| Cotización not `pendiente` (accept/reject) | 400 |
| Solicitud not `pendiente` on accept | 400 |
| Another cotización already `aceptada` on solicitud | 409 |
| Supabase/insert failure | 503 |

## Risks / Trade-offs

- **[Race] Two simultaneous accepts** → Mitigation: DB unique index on `(id_solicitud) WHERE estado = 'aceptada'`; second accept returns 409
- **[Partial update] Accept succeeds but bulk reject fails** → Mitigation: implement accept in service with ordered updates; return 503 if any step fails; repository methods should be idempotent where possible
- **[Stale UI on panel-cliente]** → Mitigation: panel loads estado on navigation; acceptable for demo without websockets
- **[Technician view]** → Cotización estado updates on reload of disponibles/detail; out of scope for live sync

## Migration Plan

1. Deploy backend with new PATCH routes (backward compatible).
2. Deploy frontend wired to PATCH.
3. Verify accept/reject on a solicitud with multiple cotizaciones in dev Supabase.
4. Rollback: revert frontend to local-only (old behavior); backend routes unused harmlessly.

## Open Questions

- None blocking — use `en_proceso` for solicitud on accept as confirmed by schema and existing frontend timeline.
