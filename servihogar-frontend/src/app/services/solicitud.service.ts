import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import {
  SolicitudDetalle,
  SolicitudDisponible,
  SolicitudListResponse,
  SolicitudRequest,
  SolicitudResponse,
} from '../models/solicitud';

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
