-- =========================================================
-- Función: rpc_exists_cotizacion_tecnico
-- Reemplaza: client.table("cotizaciones")
--              .select("id_cotizacion")
--              .eq("id_solicitud", id_solicitud)
--              .eq("id_tecnico", id_tecnico)
--              .limit(1)
-- Devuelve true si el técnico ya cotizó en esa solicitud.
-- Uso: SELECT * FROM rpc_exists_cotizacion_tecnico(1, 1);
-- =========================================================

create or replace function rpc_exists_cotizacion_tecnico(
  p_id_solicitud bigint,
  p_id_tecnico bigint
)
returns boolean
language plpgsql
stable
as $$
declare
  exists_bool boolean;
begin
  select exists(
    select 1
    from cotizaciones
    where id_solicitud = p_id_solicitud
      and id_tecnico = p_id_tecnico
  ) into exists_bool;
  return exists_bool;
end;
$$;


-- =========================================================
-- Función: rpc_get_cotizacion_by_id
-- Reemplaza: client.table("cotizaciones").select(...).eq("id_cotizacion", id).limit(1)
-- Devuelve el registro como JSON o null si no existe.
-- Uso: SELECT * FROM rpc_get_cotizacion_by_id(1);
-- =========================================================

create or replace function rpc_get_cotizacion_by_id(p_id_cotizacion bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select row_to_json(c.*)
  into result_json
  from (
    select id_cotizacion, id_solicitud, id_tecnico, monto, descripcion,
           tiempo_estimado, estado, fecha_envio
    from cotizaciones
    where id_cotizacion = p_id_cotizacion
  ) c;
  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_has_cotizacion_aceptada_solicitud
-- Reemplaza: client.table("cotizaciones")
--              .select("id_cotizacion")
--              .eq("id_solicitud", id_solicitud)
--              .eq("estado", "aceptada")
--              .limit(1)
-- Devuelve true si la solicitud ya tiene una cotización aceptada.
-- Uso: SELECT * FROM rpc_has_cotizacion_aceptada_solicitud(1);
-- =========================================================

create or replace function rpc_has_cotizacion_aceptada_solicitud(p_id_solicitud bigint)
returns boolean
language plpgsql
stable
as $$
declare
  exists_bool boolean;
begin
  select exists(
    select 1
    from cotizaciones
    where id_solicitud = p_id_solicitud
      and estado = 'aceptada'
  ) into exists_bool;
  return exists_bool;
end;
$$;


-- =========================================================
-- Función: rpc_get_cotizacion_aceptada_solicitud
-- Reemplaza: client.table("cotizaciones")
--              .select("id_cotizacion, id_solicitud, id_tecnico, estado")
--              .eq("id_solicitud", id_solicitud)
--              .eq("estado", "aceptada")
--              .limit(1)
-- Devuelve la cotización aceptada como JSON o null.
-- Uso: SELECT * FROM rpc_get_cotizacion_aceptada_solicitud(1);
-- =========================================================

create or replace function rpc_get_cotizacion_aceptada_solicitud(p_id_solicitud bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select row_to_json(c.*)
  into result_json
  from (
    select id_cotizacion, id_solicitud, id_tecnico, estado
    from cotizaciones
    where id_solicitud = p_id_solicitud
      and estado = 'aceptada'
    limit 1
  ) c;
  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_insert_cotizacion
-- Reemplaza: client.table("cotizaciones").insert(data)
-- Crea cotización con estado 'pendiente' y devuelve el registro completo.
-- Uso: SELECT * FROM rpc_insert_cotizacion(1, 1, 150.00, 'Descripción', '2 días');
-- =========================================================

create or replace function rpc_insert_cotizacion(
  p_id_solicitud bigint,
  p_id_tecnico bigint,
  p_monto numeric,
  p_descripcion text,
  p_tiempo_estimado text default null
)
returns json
language plpgsql
as $$
declare
  result_json json;
begin
  insert into cotizaciones (id_solicitud, id_tecnico, monto, descripcion, tiempo_estimado, estado)
  values (p_id_solicitud, p_id_tecnico, p_monto, p_descripcion, p_tiempo_estimado, 'pendiente')
  returning row_to_json(cotizaciones.*) into result_json;

  return result_json;
end;
$$;


-- =========================================================
-- Seguridad: solo service_role puede ejecutar estas funciones
-- =========================================================

revoke execute on function rpc_exists_cotizacion_tecnico(bigint, bigint) from public, anon, authenticated;
revoke execute on function rpc_get_cotizacion_by_id(bigint) from public, anon, authenticated;
revoke execute on function rpc_has_cotizacion_aceptada_solicitud(bigint) from public, anon, authenticated;
revoke execute on function rpc_get_cotizacion_aceptada_solicitud(bigint) from public, anon, authenticated;
revoke execute on function rpc_insert_cotizacion(bigint, bigint, numeric, text, text) from public, anon, authenticated;

grant execute on function rpc_exists_cotizacion_tecnico(bigint, bigint) to service_role;
grant execute on function rpc_get_cotizacion_by_id(bigint) to service_role;
grant execute on function rpc_has_cotizacion_aceptada_solicitud(bigint) to service_role;
grant execute on function rpc_get_cotizacion_aceptada_solicitud(bigint) to service_role;
grant execute on function rpc_insert_cotizacion(bigint, bigint, numeric, text, text) to service_role;
