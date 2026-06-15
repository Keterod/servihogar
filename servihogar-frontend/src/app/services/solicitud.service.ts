import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { SolicitudListResponse, SolicitudRequest, SolicitudResponse } from '../models/solicitud';

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
}
