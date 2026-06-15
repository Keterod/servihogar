import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { AuthService } from './auth.service';
import {
  PortafolioCreateRequest,
  PortafolioItemPanel,
  Tecnico,
  TecnicoDetalle,
} from '../models/tecnico';

export type CrearPortafolioResult =
  | PortafolioItemPanel
  | 'unauthorized'
  | 'forbidden'
  | 'validation'
  | 'limit'
  | null;

@Injectable({
  providedIn: 'root',
})
export class TecnicoService {
  private readonly http = inject(HttpClient);
  private readonly authService = inject(AuthService);

  obtenerTecnicos(): Observable<Tecnico[]> {
    return this.http.get<Tecnico[]>(`${API_BASE_URL}/tecnicos`);
  }

  obtenerTecnicoPorId(id: number): Observable<TecnicoDetalle | null> {
    return this.http.get<TecnicoDetalle>(`${API_BASE_URL}/tecnicos/${id}`).pipe(
      catchError((err: HttpErrorResponse) => {
        if (err.status === 404) {
          return of(null);
        }
        return throwError(() => err);
      }),
    );
  }

  obtenerMiPortafolio(): Observable<PortafolioItemPanel[] | null> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of(null);
    }
    return this.http
      .get<PortafolioItemPanel[]>(`${API_BASE_URL}/tecnicos/me/portafolio`, { headers })
      .pipe(catchError(() => of(null)));
  }

  crearPortafolioItem(data: PortafolioCreateRequest): Observable<CrearPortafolioResult> {
    const headers = this.authService.getAuthHeaders();
    if (!headers) {
      return of('unauthorized');
    }
    return this.http
      .post<PortafolioItemPanel>(`${API_BASE_URL}/tecnicos/me/portafolio`, data, { headers })
      .pipe(
        catchError((err: HttpErrorResponse) => {
          if (err.status === 401) {
            return of('unauthorized' as const);
          }
          if (err.status === 403) {
            return of('forbidden' as const);
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
}
