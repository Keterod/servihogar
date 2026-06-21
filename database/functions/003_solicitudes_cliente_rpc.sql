-- =========================================================
-- Función: rpc_listar_solicitudes_cliente
-- Reemplaza: client.table("solicitudes_servicio").select(...).eq("id_cliente", id_cliente)
--            + cotizaciones COUNT por solicitud
-- Incluye: categoría, zona, cantidad de cotizaciones
-- Uso:     SELECT * FROM rpc_listar_solicitudes_cliente(1);
-- =========================================================

create or replace function rpc_listar_solicitudes_cliente(p_id_cliente bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_solicitud', s.id_solicitud,
      'titulo', s.titulo,
      'descripcion', s.descripcion,
      'direccion_referencia', s.direccion_referencia,
      'estado', s.estado,
      'fecha_publicacion', s.fecha_publicacion,
      'categoria_nombre', c.nombre,
      'zona_nombre', z.nombre,
      'cotizaciones_count', (
        select count(*)::int
        from cotizaciones ct
        where ct.id_solicitud = s.id_solicitud
      )
    )
    order by s.fecha_publicacion desc
  ), '[]'::json)
  into result_json
  from solicitudes_servicio s
  join categorias_servicio c on c.id_categoria = s.id_categoria
  join zonas z on z.id_zona = s.id_zona
  where s.id_cliente = p_id_cliente;

  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_get_solicitud_cliente_by_id
-- Reemplaza: client.table("solicitudes_servicio").select(...)
--              .eq("id_solicitud", id).eq("id_cliente", id_cliente)
-- Devuelve null si no existe o no pertenece al cliente
-- Incluye: categoría, zona
-- Uso:     SELECT * FROM rpc_get_solicitud_cliente_by_id(1, 1);
-- =========================================================

create or replace function rpc_get_solicitud_cliente_by_id(
  p_id_solicitud bigint,
  p_id_cliente bigint
)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select json_build_object(
    'id_solicitud', s.id_solicitud,
    'titulo', s.titulo,
    'descripcion', s.descripcion,
    'direccion_referencia', s.direccion_referencia,
    'estado', s.estado,
    'fecha_publicacion', s.fecha_publicacion,
    'categoria_nombre', c.nombre,
    'zona_nombre', z.nombre
  )
  into result_json
  from solicitudes_servicio s
  join categorias_servicio c on c.id_categoria = s.id_categoria
  join zonas z on z.id_zona = s.id_zona
  where s.id_solicitud = p_id_solicitud
    and s.id_cliente = p_id_cliente;

  return result_json;
end;
$$;
