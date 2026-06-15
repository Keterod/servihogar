import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import {
  AdminResumen,
  TecnicoPendienteAdmin,
  TecnicoValidacionAdminResponse,
} from '../models/administrador';

export type TecnicoValidacionAdminResult =
  | TecnicoValidacionAdminResponse
  | 'not_found'
  | 'conflict'
  | null;

@Injectable({
  providedIn: 'root',
})
export class AdministradorService {
  private readonly http = inject(HttpClient);

  obtenerResumen(): Observable<AdminResumen | null> {
    return this.http
      .get<AdminResumen>(`${API_BASE_URL}/admin/demo/resumen`, {
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  obtenerTecnicosPendientes(): Observable<TecnicoPendienteAdmin[] | null> {
    return this.http
      .get<TecnicoPendienteAdmin[]>(`${API_BASE_URL}/admin/demo/tecnicos-pendientes`, {
        params: { _: Date.now().toString() },
      })
      .pipe(catchError(() => of(null)));
  }

  aprobarTecnico(idTecnico: number): Observable<TecnicoValidacionAdminResult> {
    return this.http
      .patch<TecnicoValidacionAdminResponse>(
        `${API_BASE_URL}/admin/demo/tecnicos/${idTecnico}/aprobar`,
        {},
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapValidacionError(err)));
  }

  rechazarTecnico(idTecnico: number): Observable<TecnicoValidacionAdminResult> {
    return this.http
      .patch<TecnicoValidacionAdminResponse>(
        `${API_BASE_URL}/admin/demo/tecnicos/${idTecnico}/rechazar`,
        {},
      )
      .pipe(catchError((err: HttpErrorResponse) => this._mapValidacionError(err)));
  }

  private _mapValidacionError(
    err: HttpErrorResponse,
  ): Observable<TecnicoValidacionAdminResult> {
    if (err.status === 404) {
      return of('not_found');
    }
    if (err.status === 409) {
      return of('conflict');
    }
    return of(null);
  }
}
