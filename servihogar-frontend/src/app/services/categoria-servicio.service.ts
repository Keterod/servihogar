import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../env';
import { CategoriaServicio } from '../models/categoria-servicio';

@Injectable({
  providedIn: 'root',
})
export class CategoriaServicioService {
  private readonly http = inject(HttpClient);

  obtenerCategorias(): Observable<CategoriaServicio[]> {
    return this.http.get<CategoriaServicio[]>(`${API_BASE_URL}/categorias`);
  }
}
