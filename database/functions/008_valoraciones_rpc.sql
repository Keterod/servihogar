-- =========================================================
-- Función: rpc_exists_valoracion_cotizacion
-- Reemplaza: client.table("valoraciones")
--              .select("id_valoracion")
--              .eq("id_cotizacion", id_cotizacion)
--              .limit(1)
-- Devuelve true si la cotización ya fue valorada.
-- Uso: SELECT * FROM rpc_exists_valoracion_cotizacion(1);
-- =========================================================

create or replace function rpc_exists_valoracion_cotizacion(p_id_cotizacion bigint)
returns boolean
language plpgsql
stable
as $$
declare
  exists_bool boolean;
begin
  select exists(
    select 1
    from valoraciones
    where id_cotizacion = p_id_cotizacion
  ) into exists_bool;
  return exists_bool;
end;
$$;


-- =========================================================
-- Función: rpc_insert_valoracion
-- Reemplaza: client.table("valoraciones").insert(data).select(...)
-- Inserta valoración y devuelve el registro completo como JSON.
-- Uso: SELECT * FROM rpc_insert_valoracion(1, 5, 'Buen servicio', 4, 5, 4, 5);
-- =========================================================

create or replace function rpc_insert_valoracion(
  p_id_cotizacion bigint,
  p_puntuacion integer,
  p_comentario text default null,
  p_puntualidad integer default null,
  p_calidad integer default null,
  p_precio integer default null,
  p_trato integer default null
)
returns json
language plpgsql
as $$
declare
  result_json json;
begin
  insert into valoraciones (id_cotizacion, puntuacion, comentario, puntualidad, calidad, precio, trato)
  values (p_id_cotizacion, p_puntuacion, p_comentario, p_puntualidad, p_calidad, p_precio, p_trato)
  returning row_to_json(valoraciones.*) into result_json;

  return result_json;
end;
$$;


-- =========================================================
-- Seguridad: solo service_role
-- =========================================================

revoke execute on function rpc_exists_valoracion_cotizacion(bigint) from public, anon, authenticated;
revoke execute on function rpc_insert_valoracion(bigint, integer, text, integer, integer, integer, integer) from public, anon, authenticated;

grant execute on function rpc_exists_valoracion_cotizacion(bigint) to service_role;
grant execute on function rpc_insert_valoracion(bigint, integer, text, integer, integer, integer, integer) to service_role;
