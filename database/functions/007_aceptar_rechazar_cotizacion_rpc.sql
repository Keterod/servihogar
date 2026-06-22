-- =========================================================
-- Función: rpc_aceptar_cotizacion_cliente
--
-- Reemplaza todo el flujo:
--   get_by_id + get_by_id_for_cliente + update_estado("aceptada")
--   + reject_pending_others + update_estado("en_proceso") en solicitud
--
-- Validaciones dentro de una sola transacción:
--   - Cotización existe                  → code = 'not_found'
--   - Pertenece a una solicitud del cliente → code = 'forbidden'
--   - Cotización en estado 'pendiente'   → code = 'bad_request'
--   - Solicitud en estado 'pendiente'    → code = 'bad_request'
--   - Sin otra cotización aceptada       → code = 'conflict'
--
-- Éxito: ok=true, cotizacion (JSON), solicitud_estado ('en_proceso')
-- Error: ok=false, code (string)
-- =========================================================

create or replace function rpc_aceptar_cotizacion_cliente(
  p_id_cotizacion bigint,
  p_id_cliente bigint
)
returns json
language plpgsql
as $$
declare
  v_cotizacion record;
  v_solicitud record;
  v_updated_cotizacion json;
  v_solicitud_estado text;
begin
  -- 1. Validar que la cotización exista
  select * into v_cotizacion
  from cotizaciones
  where id_cotizacion = p_id_cotizacion;

  if not found then
    return json_build_object('ok', false, 'code', 'not_found');
  end if;

  -- 2. Validar que la solicitud exista y pertenezca al cliente
  select * into v_solicitud
  from solicitudes_servicio
  where id_solicitud = v_cotizacion.id_solicitud
    and id_cliente = p_id_cliente;

  if not found then
    return json_build_object('ok', false, 'code', 'forbidden');
  end if;

  -- 3. Validar estado de la cotización
  if v_cotizacion.estado != 'pendiente' then
    return json_build_object('ok', false, 'code', 'bad_request');
  end if;

  -- 4. Validar estado de la solicitud
  if v_solicitud.estado != 'pendiente' then
    return json_build_object('ok', false, 'code', 'bad_request');
  end if;

  -- 5. Validar que no haya otra cotización aceptada
  if exists(
    select 1
    from cotizaciones
    where id_solicitud = v_cotizacion.id_solicitud
      and estado = 'aceptada'
  ) then
    return json_build_object('ok', false, 'code', 'conflict');
  end if;

  -- 6. Aceptar la cotización
  update cotizaciones
  set estado = 'aceptada'
  where id_cotizacion = p_id_cotizacion;

  -- 7. Rechazar otras cotizaciones pendientes de la misma solicitud
  update cotizaciones
  set estado = 'rechazada'
  where id_solicitud = v_cotizacion.id_solicitud
    and estado = 'pendiente'
    and id_cotizacion != p_id_cotizacion;

  -- 8. Cambiar solicitud a en_proceso
  update solicitudes_servicio
  set estado = 'en_proceso',
      fecha_actualizacion = now()
  where id_solicitud = v_cotizacion.id_solicitud;

  -- 9. Construir respuesta exitosa
  select row_to_json(c.*) into v_updated_cotizacion
  from (
    select id_cotizacion, id_solicitud, id_tecnico, monto, descripcion,
           tiempo_estimado, estado, fecha_envio
    from cotizaciones
    where id_cotizacion = p_id_cotizacion
  ) c;

  select estado into v_solicitud_estado
  from solicitudes_servicio
  where id_solicitud = v_cotizacion.id_solicitud;

  return json_build_object(
    'ok', true,
    'cotizacion', v_updated_cotizacion,
    'solicitud_estado', v_solicitud_estado
  );
end;
$$;


-- =========================================================
-- Función: rpc_rechazar_cotizacion_cliente
--
-- Reemplaza todo el flujo:
--   get_by_id + get_by_id_for_cliente + update_estado("rechazada")
--
-- Validaciones dentro de una sola transacción:
--   - Cotización existe              → code = 'not_found'
--   - Pertenece a solicitud del cliente → code = 'forbidden'
--   - Cotización en estado 'pendiente'  → code = 'bad_request'
--   - NO cambia la solicitud
--
-- Éxito: ok=true, cotizacion (JSON), solicitud_estado (sin cambios)
-- Error: ok=false, code (string)
-- =========================================================

create or replace function rpc_rechazar_cotizacion_cliente(
  p_id_cotizacion bigint,
  p_id_cliente bigint
)
returns json
language plpgsql
as $$
declare
  v_cotizacion record;
  v_solicitud record;
  v_updated_cotizacion json;
begin
  -- 1. Validar que la cotización exista
  select * into v_cotizacion
  from cotizaciones
  where id_cotizacion = p_id_cotizacion;

  if not found then
    return json_build_object('ok', false, 'code', 'not_found');
  end if;

  -- 2. Validar que la solicitud exista y pertenezca al cliente
  select * into v_solicitud
  from solicitudes_servicio
  where id_solicitud = v_cotizacion.id_solicitud
    and id_cliente = p_id_cliente;

  if not found then
    return json_build_object('ok', false, 'code', 'forbidden');
  end if;

  -- 3. Validar estado de la cotización
  if v_cotizacion.estado != 'pendiente' then
    return json_build_object('ok', false, 'code', 'bad_request');
  end if;

  -- 4. Rechazar la cotización
  update cotizaciones
  set estado = 'rechazada'
  where id_cotizacion = p_id_cotizacion;

  -- 5. Construir respuesta exitosa
  select row_to_json(c.*) into v_updated_cotizacion
  from (
    select id_cotizacion, id_solicitud, id_tecnico, monto, descripcion,
           tiempo_estimado, estado, fecha_envio
    from cotizaciones
    where id_cotizacion = p_id_cotizacion
  ) c;

  return json_build_object(
    'ok', true,
    'cotizacion', v_updated_cotizacion,
    'solicitud_estado', v_solicitud.estado
  );
end;
$$;


-- =========================================================
-- Seguridad: solo service_role puede ejecutar estas funciones
-- =========================================================

revoke execute on function rpc_aceptar_cotizacion_cliente(bigint, bigint) from public, anon, authenticated;
revoke execute on function rpc_rechazar_cotizacion_cliente(bigint, bigint) from public, anon, authenticated;

grant execute on function rpc_aceptar_cotizacion_cliente(bigint, bigint) to service_role;
grant execute on function rpc_rechazar_cotizacion_cliente(bigint, bigint) to service_role;
