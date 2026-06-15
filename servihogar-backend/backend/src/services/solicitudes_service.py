from src.repository.solicitudes_repository import SolicitudesRepository
from src.schemas.solicitud import (
    CotizacionDetalleResponse,
    SolicitudDetalleResponse,
    SolicitudListResponse,
    SolicitudRequest,
    SolicitudResponse,
)


class SolicitudesService:
    def __init__(self):
        self._repo = SolicitudesRepository()

    def crear_solicitud(self, data: SolicitudRequest) -> SolicitudResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None

        record = {
            "id_cliente": id_cliente,
            "id_categoria": data.id_categoria,
            "id_zona": data.id_zona,
            "titulo": data.titulo,
            "descripcion": data.descripcion,
            "direccion_referencia": data.direccion_referencia,
        }

        result = self._repo.insert(record)
        if result is None:
            return None

        return SolicitudResponse(
            id_solicitud=result["id_solicitud"],
            id_cliente=result["id_cliente"],
            estado=result["estado"],
            fecha_publicacion=result["fecha_publicacion"],
        )

    def obtener_por_cliente(self) -> list[SolicitudListResponse]:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return []

        rows = self._repo.get_by_cliente_id(id_cliente)
        return [
            SolicitudListResponse(
                id_solicitud=r["id_solicitud"],
                titulo=r["titulo"],
                descripcion=r["descripcion"],
                direccion=r.get("direccion_referencia"),
                estado=r["estado"],
                fecha_publicacion=r["fecha_publicacion"],
                categoria_nombre=r["categoria_nombre"],
                zona_nombre=r["zona_nombre"],
                cotizaciones_count=r["cotizaciones_count"],
            )
            for r in rows
        ]

    def obtener_detalle(self, id_solicitud: int) -> SolicitudDetalleResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None

        row = self._repo.get_by_id_for_cliente(id_solicitud, id_cliente)
        if row is None:
            return None

        cotizaciones_rows = self._repo.get_cotizaciones_by_solicitud(id_solicitud)
        cotizaciones = [
            CotizacionDetalleResponse(
                id_cotizacion=c["id_cotizacion"],
                id_tecnico=c["id_tecnico"],
                tecnico_nombre=c["tecnico_nombre"],
                tecnico_descripcion=c.get("tecnico_descripcion"),
                precio=c["precio"],
                tiempo_estimado=c.get("tiempo_estimado"),
                descripcion_propuesta=c["descripcion_propuesta"],
                estado=c["estado"],
                fecha_creacion=c["fecha_creacion"],
            )
            for c in cotizaciones_rows
        ]

        return SolicitudDetalleResponse(
            id_solicitud=row["id_solicitud"],
            titulo=row["titulo"],
            descripcion=row["descripcion"],
            direccion=row.get("direccion_referencia"),
            estado=row["estado"],
            fecha_publicacion=row["fecha_publicacion"],
            categoria_nombre=row["categoria_nombre"],
            zona_nombre=row["zona_nombre"],
            cotizaciones=cotizaciones,
        )
