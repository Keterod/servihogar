import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { AuthService } from './auth.service';
import {
  CotizacionActionResponse,
  CotizacionRequest,
  CotizacionResponse,
  ImagenSolicitud,
  ImagenSolicitudRequest,
  SolicitudDetalle,
  SolicitudDisponible,
  ServicioAceptado,
  SolicitudListResponse,
  SolicitudRequest,
  SolicitudResponse,
  ValoracionRequest,
  ValoracionResponse,
} from '../models/solicitud';

export type ObtenerDetalleResult =
  | SolicitudDetalle
  | 'unauthorized'
  | 'forbidden'
  | null;

export type CrearValoracionResult =
  | ValoracionResponse
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'bad_request'
  | 'duplicate'
  | 'validation'
  | null;

export type CrearCotizacionResult =
  | CotizacionResponse
  | 'duplicate'
  | 'not_found'
  | 'bad_request'
  | null;

export type CotizacionAccionResult =
  | CotizacionActionResponse
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'bad_request'
  | 'conflict'
  | null;

export type RegistrarImagenResult =
  | ImagenSolicitud
  | 'unauthorized'
  | 'forbidden'
  | 'not_found'
  | 'validation'
  | 'limit'
  | null;

@Injectable({
  providedIn: 'root',
})
export class SolicitudService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);

  crearSolicitud(data: SolicitudRequest): Observable<SolicitudResponse | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .post<SolicitudResponse>(`${API_BASE_URL}/solicitudes`, data, { headers })
      .pipe(catchError(() => of(null)));
  }

  registrarImagen(
    idSolicitud: number,
    data: ImagenSolicitudRequest,
  ): Observable<RegistrarImagenResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .post<ImagenSolicitud>(`${API_BASE_URL}/solicitudes/${idSolicitud}/imagenes`, data, {
        headers,
      })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
          }
          if (err.status === 404) {
            return of('not_found' as const);
          }
          if (err.status === 422) {
            return of('validation' as const);
          }
          if (err.status === 409) {
            return of('limit' as const);
          }
          return of(null);
        }),
      );
  }

  solicitudesCliente(): Observable<SolicitudListResponse[] | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .get<SolicitudListResponse[]>(`${API_BASE_URL}/clientes/me/solicitudes`, {
        headers,
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  solicitudesDisponiblesTecnico(): Observable<SolicitudDisponible[] | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .get<SolicitudDisponible[]>(`${API_BASE_URL}/tecnicos/me/solicitudes-disponibles`, {
        headers,
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  serviciosAceptadosTecnico(): Observable<ServicioAceptado[] | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .get<ServicioAceptado[]>(`${API_BASE_URL}/tecnicos/me/servicios-aceptados`, {
        headers,
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  crearCotizacion(data: CotizacionRequest): Observable<CrearCotizacionResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .post<CotizacionResponse>(`${API_BASE_URL}/cotizaciones`, data, { headers })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 409) {
            return of('duplicate' as const);
          }
          if (err.status === 404) {
            return of('not_found' as const);
          }
          if (err.status === 400 || err.status === 403) {
            return of('bad_request' as const);
          }
          return of(null);
        }),
      );
  }

  aceptarCotizacion(idCotizacion: number): Observable<CotizacionAccionResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .patch<CotizacionActionResponse>(
        `${API_BASE_URL}/cotizaciones/${idCotizacion}/aceptar`,
        {},
        { headers },
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapCotizacionAccionError(err)));
  }

  rechazarCotizacion(idCotizacion: number): Observable<CotizacionAccionResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .patch<CotizacionActionResponse>(
        `${API_BASE_URL}/cotizaciones/${idCotizacion}/rechazar`,
        {},
        { headers },
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapCotizacionAccionError(err)));
  }

  private _mapCotizacionAccionError(err: HttpErrorResponse): Observable<CotizacionAccionResult> {
    if (err.status === 401) {
      return of('unauthorized');
    }
    if (err.status === 403) {
      return of('forbidden');
    }
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

  obtenerDetalle(id: number): Observable<ObtenerDetalleResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .get<SolicitudDetalle>(`${API_BASE_URL}/solicitudes/${id}`, { headers })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
          }
          if (err.status === 404) {
            return of(null);
          }
          return throwError(() => err);
        }),
      );
  }

  crearValoracion(data: ValoracionRequest): Observable<CrearValoracionResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .post<ValoracionResponse>(`${API_BASE_URL}/valoraciones`, data, { headers })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
          }
          if (err.status === 404) {
            return of('not_found' as const);
          }
          if (err.status === 400) {
            return of('bad_request' as const);
          }
          if (err.status === 409) {
            return of('duplicate' as const);
          }
          if (err.status === 422) {
            return of('validation' as const);
          }
          return of(null);
        }),
      );
  }
}
