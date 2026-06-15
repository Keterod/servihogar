from src.repository.solicitudes_repository import SolicitudesRepository
from src.schemas.solicitud import SolicitudListResponse, SolicitudRequest, SolicitudResponse


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
