import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../env';
import { Zona } from '../models/zona';

@Injectable({
  providedIn: 'root',
})
export class ZonaService {
  private readonly http = inject(HttpClient);

  obtenerZonas(): Observable<Zona[]> {
    return this.http.get<Zona[]>(`${API_BASE_URL}/zonas`);
  }
}
