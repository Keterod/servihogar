import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { AuthService } from './auth.service';
import {
  AdminResumen,
  ReporteCotizacionItem,
  ReporteFinalizadoItem,
  ReporteSolicitudItem,
  ReporteTecnicoActivoItem,
  ReporteUsuarioItem,
  TecnicoPendienteAdmin,
  TecnicoValidacionAdminResponse,
} from '../models/administrador';

export type TecnicoValidacionAdminResult =
  | TecnicoValidacionAdminResponse
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'conflict'
  | null;

type ReporteResult<T> = T[] | 'unauthorized' | 'forbidden' | null;

@Injectable({
  providedIn: 'root',
})
export class AdministradorService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);

  obtenerResumen(): Observable<AdminResumen | 'unauthorized' | 'forbidden' | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .get<AdminResumen>(`${API_BASE_URL}/admin/demo/resumen`, {
        headers,
        params: { _: Date.now().toString() },
      })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
          }
          return of(null);
        }),
      );
  }

  obtenerTecnicosPendientes(): Observable<
    TecnicoPendienteAdmin[] | 'unauthorized' | 'forbidden' | null
  > {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .get<TecnicoPendienteAdmin[]>(`${API_BASE_URL}/admin/demo/tecnicos-pendientes`, {
        headers,
        params: { _: Date.now().toString() },
      })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
          }
          return of(null);
        }),
      );
  }

  aprobarTecnico(idTecnico: number): Observable<TecnicoValidacionAdminResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .patch<TecnicoValidacionAdminResponse>(
        `${API_BASE_URL}/admin/demo/tecnicos/${idTecnico}/aprobar`,
        {},
        { headers },
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapValidacionError(err)));
  }

  rechazarTecnico(idTecnico: number): Observable<TecnicoValidacionAdminResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .patch<TecnicoValidacionAdminResponse>(
        `${API_BASE_URL}/admin/demo/tecnicos/${idTecnico}/rechazar`,
        {},
        { headers },
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapValidacionError(err)));
  }

  obtenerReporteUsuarios(): Observable<ReporteResult<ReporteUsuarioItem>> {
    return this._obtenerReporte<ReporteUsuarioItem>(`${API_BASE_URL}/admin/demo/reportes/usuarios`);
  }

  obtenerReporteSolicitudes(): Observable<ReporteResult<ReporteSolicitudItem>> {
    return this._obtenerReporte<ReporteSolicitudItem>(`${API_BASE_URL}/admin/demo/reportes/solicitudes`);
  }

  obtenerReporteCotizaciones(): Observable<ReporteResult<ReporteCotizacionItem>> {
    return this._obtenerReporte<ReporteCotizacionItem>(`${API_BASE_URL}/admin/demo/reportes/cotizaciones`);
  }

  obtenerReporteFinalizados(): Observable<ReporteResult<ReporteFinalizadoItem>> {
    return this._obtenerReporte<ReporteFinalizadoItem>(`${API_BASE_URL}/admin/demo/reportes/finalizados`);
  }

  obtenerReporteTecnicosActivos(): Observable<ReporteResult<ReporteTecnicoActivoItem>> {
    return this._obtenerReporte<ReporteTecnicoActivoItem>(`${API_BASE_URL}/admin/demo/reportes/tecnicos-activos`);
  }

  private _obtenerReporte<T>(url: string): Observable<ReporteResult<T>> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http.get<T[]>(url, { headers, params: { _: Date.now().toString() } }).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 401) return of('unauthorized' as const);
        if (err.status === 403) return of('forbidden' as const);
        return of(null);
      }),
    );
  }

  private _mapValidacionError(
    err: HttpErrorResponse,
  ): Observable<TecnicoValidacionAdminResult> {
    if (err.status === 401) {
      return of('unauthorized');
    }
    if (err.status === 403) {
      return of('forbidden');
    }
    if (err.status === 404) {
      return of('not_found');
    }
    if (err.status === 409) {
      return of('conflict');
    }
    return of(null);
  }
}
