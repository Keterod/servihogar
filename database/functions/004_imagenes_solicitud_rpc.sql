-- =========================================================
-- Función: rpc_insert_imagen_solicitud
-- Reemplaza: client.table("imagenes_solicitud").insert(payload).select("*")
-- Inserta una imagen y devuelve el registro completo como JSON.
-- Uso: SELECT * FROM rpc_insert_imagen_solicitud(1, 'url.jpg', 'desc');
-- =========================================================

create or replace function rpc_insert_imagen_solicitud(
  p_id_solicitud bigint,
  p_imagen_url text,
  p_descripcion text default null
)
returns json
language plpgsql
as $$
declare
  result_json json;
begin
  insert into imagenes_solicitud (id_solicitud, imagen_url, descripcion)
  values (p_id_solicitud, p_imagen_url, p_descripcion)
  returning row_to_json(imagenes_solicitud.*) into result_json;

  return result_json;
end;
$$;


-- =========================================================
-- Función: rpc_count_imagenes_solicitud
-- Reemplaza: client.table("imagenes_solicitud")
--              .select("id_imagen", count="exact")
--              .eq("id_solicitud", id_solicitud)
-- Devuelve la cantidad de imágenes de una solicitud.
-- Uso: SELECT * FROM rpc_count_imagenes_solicitud(1);
-- =========================================================

create or replace function rpc_count_imagenes_solicitud(p_id_solicitud bigint)
returns integer
language plpgsql
stable
as $$
declare
  total integer;
begin
  select count(*)::integer into total
  from imagenes_solicitud
  where id_solicitud = p_id_solicitud;

  return total;
end;
$$;


-- =========================================================
-- Función: rpc_listar_imagenes_solicitud
-- Reemplaza: client.table("imagenes_solicitud")
--              .select("id_imagen, imagen_url, descripcion, fecha_subida")
--              .eq("id_solicitud", id_solicitud)
--              .order("fecha_subida")
-- Devuelve JSON array con las imágenes ordenadas por fecha.
-- Uso: SELECT * FROM rpc_listar_imagenes_solicitud(1);
-- =========================================================

create or replace function rpc_listar_imagenes_solicitud(p_id_solicitud bigint)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select coalesce(json_agg(
    json_build_object(
      'id_imagen', i.id_imagen,
      'imagen_url', i.imagen_url,
      'descripcion', i.descripcion,
      'fecha_subida', i.fecha_subida
    )
    order by i.fecha_subida
  ), '[]'::json)
  into result_json
  from imagenes_solicitud i
  where i.id_solicitud = p_id_solicitud;

  return result_json;
end;
$$;
