import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../env';
import { Tecnico } from '../models/tecnico';

@Injectable({
  providedIn: 'root',
})
export class TecnicoService {
  private readonly http = inject(HttpClient);

  obtenerTecnicos(): Observable<Tecnico[]> {
    return this.http.get<Tecnico[]>(`${API_BASE_URL}/tecnicos`);
  }
}
