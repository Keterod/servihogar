import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import { SolicitudService } from '../../services/solicitud.service';
import { CotizacionDetalle, SolicitudDetalle } from '../../models/solicitud';

@Component({
  selector: 'app-valorar-servicio',
  imports: [RouterLink],
  templateUrl: './valorar-servicio.html',
  styleUrl: './valorar-servicio.css',
})
export class ValorarServicio implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly solicitudService = inject(SolicitudService);

  readonly opcionesCalificacion = [1, 2, 3, 4, 5];

  readonly idSolicitud = signal<number | null>(null);
  readonly solicitud = signal<SolicitudDetalle | null>(null);
  readonly cotizacionAceptada = signal<CotizacionDetalle | null>(null);
  readonly cargando = signal(true);
  readonly errorCarga = signal(false);
  readonly sinId = signal(false);

  readonly puntualidad = signal(0);
  readonly calidad = signal(0);
  readonly trato = signal(0);
  readonly limpieza = signal(0);
  readonly cumplimientoPrecio = signal(0);

  readonly comentario = signal('');
  readonly volveriaContratar = signal(false);

  readonly enviando = signal(false);
  readonly enviado = signal(false);
  readonly errorEnvio = signal<string | null>(null);
  readonly duplicado = signal(false);

  readonly promedio = computed(() => {
    const valores = [
      this.puntualidad(),
      this.calidad(),
      this.trato(),
      this.limpieza(),
      this.cumplimientoPrecio(),
    ];
    const suma = valores.reduce((a, b) => a + b, 0);
    const cantidad = valores.filter((v) => v > 0).length;
    return cantidad > 0 ? (suma / cantidad).toFixed(1) : '0.0';
  });

  readonly calificacionFinal = computed(() => {
    const valores = [
      this.puntualidad(),
      this.calidad(),
      this.trato(),
      this.limpieza(),
      this.cumplimientoPrecio(),
    ];
    const cantidad = valores.filter((v) => v > 0).length;
    if (cantidad === 0) {
      return 0;
    }
    const promedio = valores.reduce((a, b) => a + b, 0) / cantidad;
    return Math.min(5, Math.max(1, Math.round(promedio)));
  });

  readonly todosCalificados = computed(() =>
    [this.puntualidad(), this.calidad(), this.trato(), this.limpieza(), this.cumplimientoPrecio()].every(
      (v) => v > 0,
    ),
  );

  readonly estadoLabel = computed(() => {
    const estado = this.solicitud()?.estado;
    const labels: Record<string, string> = {
      en_proceso: 'En proceso',
      finalizada: 'Finalizado',
    };
    return labels[estado ?? ''] ?? estado ?? '—';
  });

  readonly inicialesTecnico = computed(() => {
    const nombre = this.cotizacionAceptada()?.tecnico_nombre ?? '';
    const partes = nombre.trim().split(/\s+/).filter(Boolean);
    if (partes.length === 0) {
      return '—';
    }
    return partes
      .slice(0, 2)
      .map((p) => p[0]?.toUpperCase() ?? '')
      .join('');
  });

  ngOnInit(): void {
    const rawId = this.route.snapshot.queryParamMap.get('idSolicitud');
    const id = rawId ? Number(rawId) : NaN;
    if (!rawId || Number.isNaN(id) || id <= 0) {
      this.sinId.set(true);
      this.cargando.set(false);
      return;
    }

    this.idSolicitud.set(id);
    this.cargarSolicitud(id);
  }

  private cargarSolicitud(id: number): void {
    this.cargando.set(true);
    this.errorCarga.set(false);

    this.solicitudService.obtenerDetalle(id).subscribe({
      next: (detalle) => {
        this.cargando.set(false);
        if (detalle === null) {
          this.errorCarga.set(true);
          return;
        }
        this.solicitud.set(detalle);
        const aceptada =
          detalle.cotizaciones.find((c) => c.estado === 'aceptada') ?? null;
        this.cotizacionAceptada.set(aceptada);
      },
      error: () => {
        this.cargando.set(false);
        this.errorCarga.set(true);
      },
    });
  }

  setPuntualidad(valor: number): void {
    this.puntualidad.set(valor);
  }

  setCalidad(valor: number): void {
    this.calidad.set(valor);
  }

  setTrato(valor: number): void {
    this.trato.set(valor);
  }

  setLimpieza(valor: number): void {
    this.limpieza.set(valor);
  }

  setCumplimientoPrecio(valor: number): void {
    this.cumplimientoPrecio.set(valor);
  }

  enviarValoracion(): void {
    if (this.enviando() || this.enviado() || !this.todosCalificados()) {
      return;
    }

    const idSolicitud = this.idSolicitud();
    if (idSolicitud === null) {
      this.errorEnvio.set('No se encontró la solicitud a valorar.');
      return;
    }

    this.enviando.set(true);
    this.errorEnvio.set(null);
    this.duplicado.set(false);

    const comentario = this.comentario().trim();
    this.solicitudService
      .crearValoracion({
        id_solicitud: idSolicitud,
        calificacion: this.calificacionFinal(),
        comentario: comentario || undefined,
        puntualidad: this.puntualidad(),
        calidad: this.calidad(),
        trato: this.trato(),
        precio: this.cumplimientoPrecio(),
      })
      .subscribe((resultado) => {
        this.enviando.set(false);

        if (resultado === 'duplicate') {
          this.duplicado.set(true);
          this.errorEnvio.set('Esta solicitud ya fue valorada anteriormente.');
          return;
        }

        if (resultado === 'not_found') {
          this.errorEnvio.set('La solicitud no existe o no tienes acceso para valorarla.');
          return;
        }

        if (resultado === 'bad_request') {
          this.errorEnvio.set(
            'Esta solicitud no se puede valorar. Verifica que tenga una cotización aceptada.',
          );
          return;
        }

        if (resultado === 'validation') {
          this.errorEnvio.set('Revisa que todas las calificaciones estén entre 1 y 5.');
          return;
        }

        if (resultado === null) {
          this.errorEnvio.set(
            'No se pudo enviar la valoración. Verifica que el backend esté disponible.',
          );
          return;
        }

        this.enviado.set(true);
        this.errorEnvio.set(null);
      });
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
