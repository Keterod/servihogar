-- =========================================================
-- Función: rpc_listar_portafolio_tecnico
-- Reemplaza: client.table("portafolio_tecnico")
--              .select("id_portafolio, titulo, descripcion, imagen_url, estado, fecha_subida")
--              .eq("id_tecnico", id_tecnico)
--              .order("fecha_subida", desc=True)
-- Devuelve JSON array ordenado por fecha_subida descendente.
-- Uso: SELECT * FROM rpc_listar_portafolio_tecnico(1);
-- =========================================================

create or replace function rpc_listar_portafolio_tecnico(p_id_tecnico bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_portafolio', p.id_portafolio,
      'titulo', p.titulo,
      'descripcion', p.descripcion,
      'imagen_url', p.imagen_url,
      'estado', p.estado,
      'fecha_subida', p.fecha_subida
    )
    order by p.fecha_subida desc
  ), '[]'::json)
  into result_json
  from portafolio_tecnico p
  where p.id_tecnico = p_id_tecnico;

  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_count_portafolio_visible
-- Reemplaza: client.table("portafolio_tecnico")
--              .select("id_portafolio", count="exact")
--              .eq("id_tecnico", id_tecnico)
--              .eq("estado", "visible")
-- Devuelve la cantidad de ítems visibles del portafolio.
-- Uso: SELECT * FROM rpc_count_portafolio_visible(1);
-- =========================================================

create or replace function rpc_count_portafolio_visible(p_id_tecnico bigint)
returns integer
language plpgsql
stable
as $$
declare
  total integer;
begin
  select count(*)::integer into total
  from portafolio_tecnico
  where id_tecnico = p_id_tecnico
    and estado = 'visible';

  return total;
end;
$$;


-- =========================================================
-- Función: rpc_insert_portafolio_tecnico
-- Reemplaza: client.table("portafolio_tecnico").insert(payload).select("*")
-- Inserta un ítem con estado 'visible' y devuelve el registro completo.
-- Uso: SELECT * FROM rpc_insert_portafolio_tecnico(1, 'Título', 'Desc', 'url.jpg');
-- =========================================================

create or replace function rpc_insert_portafolio_tecnico(
  p_id_tecnico bigint,
  p_titulo text,
  p_descripcion text default null,
  p_imagen_url text
)
returns json
language plpgsql
as $$
declare
  result_json json;
begin
  insert into portafolio_tecnico (id_tecnico, titulo, descripcion, imagen_url, estado)
  values (p_id_tecnico, p_titulo, p_descripcion, p_imagen_url, 'visible')
  returning row_to_json(portafolio_tecnico.*) into result_json;

  return result_json;
end;
$$;


-- =========================================================
-- Seguridad: solo service_role puede ejecutar estas funciones
-- =========================================================

revoke execute on function rpc_listar_portafolio_tecnico(bigint) from public, anon, authenticated;
revoke execute on function rpc_count_portafolio_visible(bigint) from public, anon, authenticated;
revoke execute on function rpc_insert_portafolio_tecnico(bigint, text, text, text) from public, anon, authenticated;

grant execute on function rpc_listar_portafolio_tecnico(bigint) to service_role;
grant execute on function rpc_count_portafolio_visible(bigint) to service_role;
grant execute on function rpc_insert_portafolio_tecnico(bigint, text, text, text) to service_role;
