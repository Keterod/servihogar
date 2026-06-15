import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import {
  CotizacionActionResponse,
  CotizacionRequest,
  CotizacionResponse,
  SolicitudDetalle,
  SolicitudDisponible,
  ServicioAceptado,
  SolicitudListResponse,
  SolicitudRequest,
  SolicitudResponse,
} from '../models/solicitud';

export type CrearCotizacionResult =
  | CotizacionResponse
  | 'duplicate'
  | 'not_found'
  | 'bad_request'
  | null;

export type CotizacionAccionResult =
  | CotizacionActionResponse
  | 'not_found'
  | 'bad_request'
  | 'conflict'
  | null;

@Injectable({
  providedIn: 'root',
})
export class SolicitudService {
  private readonly http = inject(HttpClient);

  crearSolicitud(data: SolicitudRequest): Observable<SolicitudResponse | null> {
    return this.http.post<SolicitudResponse>(`${API_BASE_URL}/solicitudes`, data).pipe(
      catchError(() => of(null)),
    );
  }

  solicitudesCliente(): Observable<SolicitudListResponse[] | null> {
    return this.http
      .get<SolicitudListResponse[]>(`${API_BASE_URL}/clientes/demo/solicitudes`, {
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  solicitudesDisponiblesTecnico(): Observable<SolicitudDisponible[] | null> {
    return this.http
      .get<SolicitudDisponible[]>(`${API_BASE_URL}/tecnicos/demo/solicitudes-disponibles`, {
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  serviciosAceptadosTecnico(): Observable<ServicioAceptado[] | null> {
    return this.http
      .get<ServicioAceptado[]>(`${API_BASE_URL}/tecnicos/demo/servicios-aceptados`, {
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  crearCotizacion(data: CotizacionRequest): Observable<CrearCotizacionResult> {
    return this.http.post<CotizacionResponse>(`${API_BASE_URL}/cotizaciones`, data).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 409) {
          return of('duplicate' as const);
        }
        if (err.status === 404) {
          return of('not_found' as const);
        }
        if (err.status === 400) {
          return of('bad_request' as const);
        }
        return of(null);
      }),
    );
  }

  aceptarCotizacion(idCotizacion: number): Observable<CotizacionAccionResult> {
    return this.http
      .patch<CotizacionActionResponse>(
        `${API_BASE_URL}/cotizaciones/${idCotizacion}/aceptar`,
        {},
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapCotizacionAccionError(err)));
  }

  rechazarCotizacion(idCotizacion: number): Observable<CotizacionAccionResult> {
    return this.http
      .patch<CotizacionActionResponse>(
        `${API_BASE_URL}/cotizaciones/${idCotizacion}/rechazar`,
        {},
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapCotizacionAccionError(err)));
  }

  private _mapCotizacionAccionError(err: HttpErrorResponse): Observable<CotizacionAccionResult> {
    if (err.status === 404) {
      return of('not_found');
    }
    if (err.status === 400) {
      return of('bad_request');
    }
    if (err.status === 409) {
      return of('conflict');
    }
    return of(null);
  }

  obtenerDetalle(id: number): Observable<SolicitudDetalle | null> {
    return this.http.get<SolicitudDetalle>(`${API_BASE_URL}/solicitudes/${id}`).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 404) {
          return of(null);
        }
        return throwError(() => err);
      }),
    );
  }
}
