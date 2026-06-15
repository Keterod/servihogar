from typing import Literal

from src.repository.cotizaciones_repository import CotizacionesRepository
from src.repository.imagenes_solicitud_repository import ImagenesSolicitudRepository
from src.repository.solicitudes_repository import SolicitudesRepository
from src.repository.tecnicos_repository import TecnicosRepository
from src.schemas.auth import AuthMeResponse, TipoUsuario
from src.schemas.solicitud import (
    CotizacionDetalleResponse,
    ImagenSolicitudRequest,
    ImagenSolicitudResponse,
    ServicioAceptadoResponse,
    SolicitudDetalleResponse,
    SolicitudDisponibleResponse,
    SolicitudListResponse,
    SolicitudRequest,
    SolicitudResponse,
)

MAX_IMAGENES_POR_SOLICITUD = 5
ALLOWED_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")


class ImagenError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


class SolicitudesService:
    def __init__(self):
        self._repo = SolicitudesRepository()
        self._tecnicos_repo = TecnicosRepository()
        self._cotizaciones_repo = CotizacionesRepository()
        self._imagenes_repo = ImagenesSolicitudRepository()

    @staticmethod
    def _validar_imagen_url(imagen_url: str, prefix: str) -> None:
        if ".." in imagen_url or imagen_url.startswith("/"):
            raise ImagenError("validation", "Ruta de imagen inválida")
        if not imagen_url.startswith(prefix):
            raise ImagenError(
                "validation",
                f"La imagen debe estar bajo el prefijo {prefix}",
            )
        lower = imagen_url.lower()
        if not any(lower.endswith(ext) for ext in ALLOWED_IMAGE_SUFFIXES):
            raise ImagenError(
                "validation",
                "Solo se permiten imágenes JPEG, PNG o WebP",
            )

    @staticmethod
    def _to_imagen_response(row: dict) -> ImagenSolicitudResponse:
        return ImagenSolicitudResponse(
            id_imagen=row["id_imagen"],
            imagen_url=row["imagen_url"],
            descripcion=row.get("descripcion"),
            fecha_subida=row["fecha_subida"],
        )

    def registrar_imagen(
        self, id_solicitud: int, id_cliente: int, data: ImagenSolicitudRequest
    ) -> ImagenSolicitudResponse:
        row = self._repo.get_solicitud_by_id(id_solicitud)
        if row is None:
            raise ImagenError("not_found", "Solicitud no encontrada")
        if int(row["id_cliente"]) != id_cliente:
            raise ImagenError(
                "forbidden",
                "No tienes permiso para agregar imágenes a esta solicitud",
            )

        prefix = f"solicitudes/{id_solicitud}/"
        self._validar_imagen_url(data.imagen_url, prefix)

        count = self._imagenes_repo.count_by_solicitud(id_solicitud)
        if count >= MAX_IMAGENES_POR_SOLICITUD:
            raise ImagenError(
                "limit",
                f"Máximo {MAX_IMAGENES_POR_SOLICITUD} imágenes por solicitud",
            )

        inserted = self._imagenes_repo.insert(
            id_solicitud, data.imagen_url, data.descripcion
        )
        if inserted is None:
            raise ImagenError("failed", "No se pudo registrar la imagen")

        return self._to_imagen_response(inserted)

    def listar_imagenes(self, id_solicitud: int) -> list[ImagenSolicitudResponse]:
        rows = self._imagenes_repo.list_by_solicitud(id_solicitud)
        return [self._to_imagen_response(r) for r in rows]

    def crear_solicitud(self, data: SolicitudRequest) -> SolicitudResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None
        return self.crear_solicitud_para_cliente(id_cliente, data)

    def crear_solicitud_para_cliente(
        self, id_cliente: int, data: SolicitudRequest
    ) -> SolicitudResponse | None:
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
        return self.obtener_por_cliente_id(id_cliente)

    def obtener_por_cliente_id(self, id_cliente: int) -> list[SolicitudListResponse]:
        rows = self._repo.get_by_cliente_id(id_cliente)
        return [self._to_list_response(r) for r in rows]

    @staticmethod
    def _to_list_response(row: dict) -> SolicitudListResponse:
        return SolicitudListResponse(
            id_solicitud=row["id_solicitud"],
            titulo=row["titulo"],
            descripcion=row["descripcion"],
            direccion=row.get("direccion_referencia"),
            estado=row["estado"],
            fecha_publicacion=row["fecha_publicacion"],
            categoria_nombre=row["categoria_nombre"],
            zona_nombre=row["zona_nombre"],
            cotizaciones_count=row["cotizaciones_count"],
        )

    def verificar_acceso_detalle(
        self, id_solicitud: int, user: AuthMeResponse
    ) -> Literal["ok", "not_found", "forbidden"]:
        row = self._repo.get_solicitud_by_id(id_solicitud)
        if row is None:
            return "not_found"

        if user.tipo_usuario == TipoUsuario.administrador:
            return "ok"

        if user.tipo_usuario == TipoUsuario.cliente:
            if user.id_cliente is None or row["id_cliente"] != user.id_cliente:
                return "forbidden"
            return "ok"

        if user.tipo_usuario == TipoUsuario.tecnico:
            if user.id_tecnico is None:
                return "forbidden"
            if self._tecnico_puede_ver_solicitud(id_solicitud, user.id_tecnico, row):
                return "ok"
            return "forbidden"

        return "forbidden"

    def _tecnico_puede_ver_solicitud(
        self, id_solicitud: int, id_tecnico: int, row: dict
    ) -> bool:
        if self._cotizaciones_repo.exists_for_tecnico(id_solicitud, id_tecnico):
            return True

        categorias = self._tecnicos_repo.get_categorias_for_tecnico(id_tecnico)
        zonas = self._tecnicos_repo.get_zonas_for_tecnico(id_tecnico)
        if self._repo.get_solicitud_for_cotizacion(id_solicitud, categorias, zonas):
            return True

        return False

    def obtener_detalle_por_id(self, id_solicitud: int) -> SolicitudDetalleResponse | None:
        row = self._repo.get_by_id(id_solicitud)
        if row is None:
            return None
        return self._build_detalle_response(row, id_solicitud)

    def _build_detalle_response(
        self, row: dict, id_solicitud: int
    ) -> SolicitudDetalleResponse:
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

        imagenes_rows = self._imagenes_repo.list_by_solicitud(id_solicitud)
        imagenes = [self._to_imagen_response(r) for r in imagenes_rows]

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
            imagenes=imagenes,
        )

    def obtener_detalle(self, id_solicitud: int) -> SolicitudDetalleResponse | None:
        id_cliente = self._repo.get_demo_cliente_id()
        if id_cliente is None:
            return None

        row = self._repo.get_by_id_for_cliente(id_solicitud, id_cliente)
        if row is None:
            return None

        return self._build_detalle_response(row, id_solicitud)

    def obtener_solicitudes_disponibles_demo(self) -> list[SolicitudDisponibleResponse]:
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            return []
        return self.obtener_solicitudes_disponibles_para_tecnico(id_tecnico)

    def obtener_solicitudes_disponibles_para_tecnico(
        self, id_tecnico: int
    ) -> list[SolicitudDisponibleResponse]:
        categorias = self._tecnicos_repo.get_categorias_for_tecnico(id_tecnico)
        zonas = self._tecnicos_repo.get_zonas_for_tecnico(id_tecnico)
        rows = self._repo.get_disponibles_for_tecnico(id_tecnico, categorias, zonas)

        return [
            SolicitudDisponibleResponse(
                id_solicitud=r["id_solicitud"],
                titulo=r["titulo"],
                descripcion=r["descripcion"],
                direccion=r.get("direccion_referencia"),
                estado=r["estado"],
                fecha_publicacion=r["fecha_publicacion"],
                categoria_nombre=r["categoria_nombre"],
                zona_nombre=r["zona_nombre"],
                cliente_nombre=r.get("cliente_nombre"),
                cotizaciones_count=r["cotizaciones_count"],
                ya_cotizada_por_tecnico=r["ya_cotizada_por_tecnico"],
            )
            for r in rows
        ]

    def obtener_servicios_aceptados_demo(self) -> list[ServicioAceptadoResponse]:
        id_tecnico = self._tecnicos_repo.get_demo_tecnico_id()
        if id_tecnico is None:
            return []
        return self.obtener_servicios_aceptados_para_tecnico(id_tecnico)

    def obtener_servicios_aceptados_para_tecnico(
        self, id_tecnico: int
    ) -> list[ServicioAceptadoResponse]:
        try:
            rows = self._repo.get_servicios_aceptados_for_tecnico(id_tecnico)
        except Exception:
            return []

        servicios: list[ServicioAceptadoResponse] = []
        for r in rows:
            try:
                servicios.append(
                    ServicioAceptadoResponse(
                        id_solicitud=r["id_solicitud"],
                        titulo=r.get("titulo") or "",
                        descripcion=r.get("descripcion") or "",
                        direccion=r.get("direccion_referencia"),
                        estado=r.get("estado") or "",
                        fecha_publicacion=r["fecha_publicacion"],
                        categoria_nombre=r.get("categoria_nombre") or "",
                        zona_nombre=r.get("zona_nombre") or "",
                        cliente_nombre=r.get("cliente_nombre"),
                        id_cotizacion=r["id_cotizacion"],
                        precio=r["precio"],
                        tiempo_estimado=r.get("tiempo_estimado"),
                        estado_cotizacion=r.get("estado_cotizacion") or "",
                    )
                )
            except Exception:
                continue

        return servicios
