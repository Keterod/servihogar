-- =========================================================
-- Función: rpc_listar_categorias
-- Reemplaza: client.table("categorias_servicio").select(...).eq("estado", "activo")
-- Uso:       SELECT * FROM rpc_listar_categorias();
-- =========================================================

create or replace function rpc_listar_categorias()
returns table(
    id_categoria bigint,
    nombre varchar(100),
    descripcion text,
    estado varchar(20),
    fecha_creacion timestamp with time zone
)
language plpgsql
stable
as $$
begin
    return query
    select
        cs.id_categoria,
        cs.nombre,
        cs.descripcion,
        cs.estado,
        cs.fecha_creacion
    from categorias_servicio cs
    where cs.estado = 'activo'
    order by cs.nombre;
end;
$$;

-- =========================================================
-- Función: rpc_listar_zonas
-- Reemplaza: client.table("zonas").select(...).eq("estado", "activo")
-- Uso:       SELECT * FROM rpc_listar_zonas();
-- =========================================================

create or replace function rpc_listar_zonas()
returns table(
    id_zona bigint,
    id_ciudad bigint,
    nombre varchar(100),
    estado varchar(20)
)
language plpgsql
stable
as $$
begin
    return query
    select
        z.id_zona,
        z.id_ciudad,
        z.nombre,
        z.estado
    from zonas z
    where z.estado = 'activo'
    order by z.nombre;
end;
$$;
