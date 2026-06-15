import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { forkJoin } from 'rxjs';

import { AdminResumen, TecnicoPendienteAdmin } from '../../models/administrador';
import {
  AdministradorService,
  TecnicoValidacionAdminResult,
} from '../../services/administrador.service';

interface MetricaAdmin {
  etiqueta: string;
  valor: number;
}

@Component({
  selector: 'app-panel-administrador',
  standalone: true,
  imports: [],
  templateUrl: './panel-administrador.html',
  styleUrl: './panel-administrador.css',
})
export class PanelAdministrador implements OnInit {
  private readonly administradorService = inject(AdministradorService);

  readonly resumen = signal<AdminResumen | null>(null);
  readonly tecnicosPendientes = signal<TecnicoPendienteAdmin[]>([]);
  readonly cargando = signal<boolean>(false);
  readonly error = signal<string | null>(null);
  readonly accionEnCurso = signal<number | null>(null);
  readonly mensajeAccion = signal<string | null>(null);

  readonly tieneDatos = computed(() => this.resumen() !== null && !this.error());
  readonly sinPendientes = computed(
    () => this.tieneDatos() && this.tecnicosPendientes().length === 0,
  );

  readonly metricasResumen = computed<MetricaAdmin[]>(() => {
    const resumen = this.resumen();
    if (!resumen) {
      return [];
    }

    return [
      { etiqueta: 'Usuarios', valor: resumen.total_usuarios },
      { etiqueta: 'Clientes', valor: resumen.total_clientes },
      { etiqueta: 'Técnicos', valor: resumen.total_tecnicos },
      { etiqueta: 'Solicitudes', valor: resumen.total_solicitudes },
      { etiqueta: 'Pendientes', valor: resumen.solicitudes_pendientes },
      { etiqueta: 'En proceso', valor: resumen.solicitudes_en_proceso },
      { etiqueta: 'Finalizadas', valor: resumen.solicitudes_finalizadas },
      { etiqueta: 'Técnicos pendientes', valor: resumen.tecnicos_pendientes },
      { etiqueta: 'Técnicos validados', valor: resumen.tecnicos_validados },
      { etiqueta: 'Técnicos rechazados', valor: resumen.tecnicos_rechazados },
      { etiqueta: 'Cotizaciones', valor: resumen.total_cotizaciones },
      { etiqueta: 'Valoraciones', valor: resumen.total_valoraciones },
    ];
  });

  readonly metricasReportes = computed<MetricaAdmin[]>(() => {
    const resumen = this.resumen();
    if (!resumen) {
      return [];
    }

    return [
      { etiqueta: 'Solicitudes publicadas', valor: resumen.total_solicitudes },
      { etiqueta: 'Cotizaciones registradas', valor: resumen.total_cotizaciones },
      { etiqueta: 'Servicios finalizados', valor: resumen.solicitudes_finalizadas },
      { etiqueta: 'Técnicos activos', valor: resumen.tecnicos_validados },
      { etiqueta: 'Usuarios registrados', valor: resumen.total_usuarios },
    ];
  });

  ngOnInit(): void {
    this.cargarDatos();
  }

  cargarDatos(): void {
    this.cargando.set(true);
    this.error.set(null);

    forkJoin({
      resumen: this.administradorService.obtenerResumen(),
      tecnicos: this.administradorService.obtenerTecnicosPendientes(),
    }).subscribe(({ resumen, tecnicos }) => {
      this.cargando.set(false);

      if (!resumen || !tecnicos) {
        this.error.set('No se pudo cargar el panel administrador. Inténtalo nuevamente.');
        return;
      }

      this.resumen.set(resumen);
      this.tecnicosPendientes.set(tecnicos);
    });
  }

  validarTecnico(idTecnico: number): void {
    this.procesarTecnico(idTecnico, 'aprobar');
  }

  rechazarTecnico(idTecnico: number): void {
    this.procesarTecnico(idTecnico, 'rechazar');
  }

  nombreCompleto(tecnico: TecnicoPendienteAdmin): string {
    return `${tecnico.nombres} ${tecnico.apellidos}`.trim();
  }

  textoLista(valores: string[]): string {
    return valores.length > 0 ? valores.join(', ') : 'Sin datos registrados';
  }

  fechaCorta(fecha: string): string {
    return new Intl.DateTimeFormat('es-PE', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    }).format(new Date(fecha));
  }

  private procesarTecnico(idTecnico: number, accion: 'aprobar' | 'rechazar'): void {
    if (this.accionEnCurso() !== null) {
      return;
    }

    this.accionEnCurso.set(idTecnico);
    this.error.set(null);
    this.mensajeAccion.set(null);

    const request =
      accion === 'aprobar'
        ? this.administradorService.aprobarTecnico(idTecnico)
        : this.administradorService.rechazarTecnico(idTecnico);

    request.subscribe((resultado) => {
      this.accionEnCurso.set(null);
      this.procesarResultadoAccion(resultado, accion);
    });
  }

  private procesarResultadoAccion(
    resultado: TecnicoValidacionAdminResult,
    accion: 'aprobar' | 'rechazar',
  ): void {
    if (!resultado) {
      this.error.set('No se pudo actualizar el técnico. Inténtalo nuevamente.');
      return;
    }

    if (resultado === 'not_found') {
      this.error.set('El técnico ya no existe o no está disponible.');
      this.cargarDatos();
      return;
    }

    if (resultado === 'conflict') {
      this.error.set('El técnico ya fue procesado. Actualizando la lista.');
      this.cargarDatos();
      return;
    }

    const mensaje =
      accion === 'aprobar'
        ? 'Técnico aprobado correctamente.'
        : 'Técnico rechazado correctamente.';
    this.mensajeAccion.set(mensaje);
    this.cargarDatos();
  }
}
