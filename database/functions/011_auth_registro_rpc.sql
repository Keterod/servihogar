-- =========================================================
-- rpc_auth_get_profile_by_auth_user_id(p_auth_user_id uuid)
-- Reemplaza: client.table("usuarios").select("id_usuario, ..., clientes(id_cliente), tecnicos(...), administradores(...)").eq("auth_user_id", id)
-- Devuelve:  perfil completo con arrays de clientes/tecnicos/administradores, o null si no existe
-- Uso:       SELECT * FROM rpc_auth_get_profile_by_auth_user_id('eb65fb3b-d00b-40b5-82e8-933cd3cd346c');
-- =========================================================

create or replace function rpc_auth_get_profile_by_auth_user_id(p_auth_user_id uuid)
returns json
language plpgsql
stable
as $$
declare
  result_json json;
begin
  select json_build_object(
    'id_usuario', u.id_usuario,
    'auth_user_id', u.auth_user_id,
    'nombres', u.nombres,
    'apellidos', u.apellidos,
    'telefono', u.telefono,
    'estado', u.estado,
    'clientes', coalesce(
      (select json_agg(json_build_object('id_cliente', c.id_cliente))
       from clientes c where c.id_usuario = u.id_usuario),
      '[]'::json
    ),
    'tecnicos', coalesce(
      (select json_agg(json_build_object('id_tecnico', t.id_tecnico, 'estado_validacion', t.estado_validacion))
       from tecnicos t where t.id_usuario = u.id_usuario),
      '[]'::json
    ),
    'administradores', coalesce(
      (select json_agg(json_build_object('id_administrador', a.id_administrador))
       from administradores a where a.id_usuario = u.id_usuario),
      '[]'::json
    )
  )
  into result_json
  from usuarios u
  where u.auth_user_id = p_auth_user_id;

  return result_json;
end;
$$;

-- =========================================================
-- rpc_auth_insert_cliente(
--   p_auth_user_id uuid,
--   p_nombres text,
--   p_apellidos text,
--   p_telefono text default null,
--   p_foto_perfil_url text default null
-- )
-- Reemplaza: insert_usuario() + insert_cliente()
-- Inserta:   usuarios + clientes en una transacción
-- Devuelve:  { ok: true, usuario: { id_usuario, auth_user_id }, cliente: { id_cliente } }
--            o { ok: false, code: 'duplicate' } si auth_user_id ya existe
-- Uso:       SELECT * FROM rpc_auth_insert_cliente('uuid', 'Juan', 'Pérez', '999888777');
-- =========================================================

create or replace function rpc_auth_insert_cliente(
  p_auth_user_id uuid,
  p_nombres text,
  p_apellidos text,
  p_telefono text default null,
  p_foto_perfil_url text default null
)
returns json
language plpgsql
as $$
declare
  v_id_usuario bigint;
  v_id_cliente bigint;
begin
  if exists(select 1 from usuarios where auth_user_id = p_auth_user_id) then
    return json_build_object('ok', false, 'code', 'duplicate');
  end if;

  insert into usuarios (auth_user_id, nombres, apellidos, telefono, foto_perfil_url, estado)
  values (p_auth_user_id, p_nombres, p_apellidos, p_telefono, p_foto_perfil_url, 'activo')
  returning id_usuario into v_id_usuario;

  insert into clientes (id_usuario, estado)
  values (v_id_usuario, 'activo')
  returning id_cliente into v_id_cliente;

  return json_build_object(
    'ok', true,
    'usuario', json_build_object('id_usuario', v_id_usuario, 'auth_user_id', p_auth_user_id),
    'cliente', json_build_object('id_cliente', v_id_cliente)
  );
end;
$$;

-- =========================================================
-- rpc_auth_insert_tecnico(
--   p_auth_user_id uuid,
--   p_nombres text,
--   p_apellidos text,
--   p_telefono text default null,
--   p_descripcion text default '',
--   p_experiencia_anios integer default 0,
--   p_categoria_ids bigint[] default '{}',
--   p_zona_ids bigint[] default '{}',
--   p_foto_perfil_url text default null
-- )
-- Reemplaza: insert_usuario() + insert_tecnico() + insert_tecnico_categorias() + insert_tecnico_zonas()
-- Inserta:   usuarios + tecnicos + tecnico_categorias + tecnico_zonas en una transacción
-- Devuelve:  { ok: true, usuario: { id_usuario, auth_user_id }, tecnico: { id_tecnico, estado_validacion } }
--            o { ok: false, code: 'duplicate' } si auth_user_id ya existe
-- Uso:       SELECT * FROM rpc_auth_insert_tecnico('uuid', 'Pedro', 'López', '999888777', 'Descripción', 3, '{1,2}', '{1}');
-- =========================================================

create or replace function rpc_auth_insert_tecnico(
  p_auth_user_id uuid,
  p_nombres text,
  p_apellidos text,
  p_telefono text default null,
  p_descripcion text default '',
  p_experiencia_anios integer default 0,
  p_categoria_ids bigint[] default '{}',
  p_zona_ids bigint[] default '{}',
  p_foto_perfil_url text default null
)
returns json
language plpgsql
as $$
declare
  v_id_usuario bigint;
  v_id_tecnico bigint;
  v_cat_id bigint;
  v_zona_id bigint;
begin
  if exists(select 1 from usuarios where auth_user_id = p_auth_user_id) then
    return json_build_object('ok', false, 'code', 'duplicate');
  end if;

  insert into usuarios (auth_user_id, nombres, apellidos, telefono, foto_perfil_url, estado)
  values (p_auth_user_id, p_nombres, p_apellidos, p_telefono, p_foto_perfil_url, 'activo')
  returning id_usuario into v_id_usuario;

  insert into tecnicos (id_usuario, descripcion, experiencia_anios, estado_validacion)
  values (v_id_usuario, p_descripcion, p_experiencia_anios, 'pendiente')
  returning id_tecnico into v_id_tecnico;

  if array_length(p_categoria_ids, 1) > 0 then
    foreach v_cat_id in array p_categoria_ids
    loop
      insert into tecnico_categorias (id_tecnico, id_categoria)
      values (v_id_tecnico, v_cat_id);
    end loop;
  end if;

  if array_length(p_zona_ids, 1) > 0 then
    foreach v_zona_id in array p_zona_ids
    loop
      insert into tecnico_zonas (id_tecnico, id_zona)
      values (v_id_tecnico, v_zona_id);
    end loop;
  end if;

  return json_build_object(
    'ok', true,
    'usuario', json_build_object('id_usuario', v_id_usuario, 'auth_user_id', p_auth_user_id),
    'tecnico', json_build_object('id_tecnico', v_id_tecnico, 'estado_validacion', 'pendiente')
  );
end;
$$;

-- =========================================================
-- rpc_auth_delete_usuario_by_auth_user_id(p_auth_user_id uuid)
-- Reemplaza: client.table("usuarios").delete().eq("id_usuario", id)
-- Elimina:   usuario (y cascadea clientes/tecnicos/categorias/zonas)
-- Devuelve:  { ok: true } (aunque no exista)
-- Uso:       SELECT * FROM rpc_auth_delete_usuario_by_auth_user_id('uuid');
-- =========================================================

create or replace function rpc_auth_delete_usuario_by_auth_user_id(p_auth_user_id uuid)
returns json
language plpgsql
as $$
begin
  delete from usuarios where auth_user_id = p_auth_user_id;
  return json_build_object('ok', true);
end;
$$;

-- =========================================================
-- Grants (solo service_role)
-- =========================================================

grant execute on function rpc_auth_get_profile_by_auth_user_id(uuid) to service_role;
grant execute on function rpc_auth_insert_cliente(uuid, text, text, text, text) to service_role;
grant execute on function rpc_auth_insert_tecnico(uuid, text, text, text, text, integer, bigint[], bigint[], text) to service_role;
grant execute on function rpc_auth_delete_usuario_by_auth_user_id(uuid) to service_role;
