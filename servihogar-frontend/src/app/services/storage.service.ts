import { Injectable, inject } from '@angular/core';

import { AuthService } from './auth.service';
import { SUPABASE_URL } from '../supabase.env';

export const STORAGE_BUCKET = 'servihogar-evidencias';
export const MAX_FILE_BYTES = 5 * 1024 * 1024;
export const MAX_SOLICITUD_IMAGES = 5;
export const MAX_PORTFOLIO_ITEMS = 20;
export const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export type UploadResult = { path: string } | { error: string };

@Injectable({
  providedIn: 'root',
})
export class StorageService {
  private readonly authService = inject(AuthService);

  validateImageFile(file: File): string | null {
    if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
      return 'Solo se permiten imágenes JPG, PNG o WebP.';
    }
    if (file.size > MAX_FILE_BYTES) {
      return 'El archivo supera el límite de 5 MB.';
    }
    return null;
  }

  sanitizeFileName(name: string): string {
    return name.replace(/[^a-zA-Z0-9._-]/g, '_').slice(0, 80);
  }

  buildSolicitudPath(idSolicitud: number, fileName: string): string {
    return `solicitudes/${idSolicitud}/${Date.now()}-${this.sanitizeFileName(fileName)}`;
  }

  buildPortafolioPath(idTecnico: number, fileName: string): string {
    return `tecnicos/${idTecnico}/portafolio/${Date.now()}-${this.sanitizeFileName(fileName)}`;
  }

  resolvePublicUrl(pathOrUrl: string): string {
    if (pathOrUrl.startsWith('http://') || pathOrUrl.startsWith('https://')) {
      return pathOrUrl;
    }
    const { data } = this.authService
      .getSupabase()
      .storage.from(STORAGE_BUCKET)
      .getPublicUrl(pathOrUrl);
    return data.publicUrl;
  }

  resolveMediaUrl(imagenUrl: string, storagePath?: string | null): string {
    if (storagePath) {
      return this.resolvePublicUrl(storagePath);
    }
    return this.resolvePublicUrl(imagenUrl);
  }

  async uploadFile(path: string, file: File): Promise<UploadResult> {
    const validationError = this.validateImageFile(file);
    if (validationError) {
      return { error: validationError };
    }

    const session = this.authService.getSession();
    if (!session) {
      return { error: 'Debes iniciar sesión para subir archivos.' };
    }

    const { error } = await this.authService
      .getSupabase()
      .storage.from(STORAGE_BUCKET)
      .upload(path, file, { upsert: false, contentType: file.type });

    if (error) {
      return { error: error.message };
    }

    return { path };
  }

  async removeFile(path: string): Promise<void> {
    await this.authService.getSupabase().storage.from(STORAGE_BUCKET).remove([path]);
  }

  getBucketPublicBaseUrl(): string {
    return `${SUPABASE_URL}/storage/v1/object/public/${STORAGE_BUCKET}`;
  }
}
