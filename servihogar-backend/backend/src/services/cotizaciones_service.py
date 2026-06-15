from src.repository.cotizaciones_repository import CotizacionesRepository
from src.repository.solicitudes_repository import SolicitudesRepository
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.cotizacion import CotizacionRequest, CotizacionResponse


class CotizacionError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class CotizacionesService:
    def __init__(self):
        self._repo = CotizacionesRepository()
        self._solicitudes_repo = SolicitudesRepository()
        self._tecnicos_repo = TecnicosRepository()

    def crear_cotizacion_demo(self, data: CotizacionRequest) -> CotizacionResponse:
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            raise CotizacionError("failed", "Técnico demo no disponible")

        categorias = self._tecnicos_repo.get_categorias_for_tecnico(id_tecnico)
        zonas = self._tecnicos_repo.get_zonas_for_tecnico(id_tecnico)

        solicitud = self._solicitudes_repo.get_solicitud_for_cotizacion(
            data.id_solicitud, categorias, zonas
        )
        if solicitud is None:
            exists = self._solicitudes_repo.get_solicitud_by_id(data.id_solicitud)
            if exists is None:
                raise CotizacionError("not_found", "Solicitud no encontrada")
            if exists["estado"] != "pendiente":
                raise CotizacionError(
                    "bad_request",
                    "Solo se pueden cotizar solicitudes en estado pendiente",
                )
            raise CotizacionError(
                "bad_request",
                "La solicitud no corresponde a las categorías o zonas del técnico demo",
            )

        if self._repo.exists_for_tecnico(data.id_solicitud, id_tecnico):
            raise CotizacionError(
                "duplicate",
                "Ya enviaste una cotización para esta solicitud",
            )

        record = {
            "id_solicitud": data.id_solicitud,
            "id_tecnico": id_tecnico,
            "monto": data.precio,
            "descripcion": data.descripcion_propuesta,
            "tiempo_estimado": data.tiempo_estimado,
        }
        result = self._repo.insert(record)
        if result is None:
            raise CotizacionError("failed", "No se pudo crear la cotización")

        return CotizacionResponse(
            id_cotizacion=result["id_cotizacion"],
            id_solicitud=result["id_solicitud"],
            id_tecnico=result["id_tecnico"],
            precio=float(result["monto"]),
            tiempo_estimado=result.get("tiempo_estimado"),
            descripcion_propuesta=result["descripcion"],
            estado=result["estado"],
            fecha_creacion=result["fecha_envio"],
        )
