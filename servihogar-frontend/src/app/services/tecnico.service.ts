import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { Tecnico, TecnicoDetalle } from '../models/tecnico';

@Injectable({
  providedIn: 'root',
})
export class TecnicoService {
  private readonly http = inject(HttpClient);

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
}
