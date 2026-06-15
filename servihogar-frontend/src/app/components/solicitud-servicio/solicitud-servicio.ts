import { Component, OnInit, computed, inject, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { firstValueFrom } from 'rxjs';

import { CategoriaServicioService } from '../../services/categoria-servicio.service';
import { ZonaService } from '../../services/zona.service';
import { SolicitudService } from '../../services/solicitud.service';
import {
  MAX_SOLICITUD_IMAGES,
  StorageService,
} from '../../services/storage.service';
import { CategoriaServicio } from '../../models/categoria-servicio';
import { Zona } from '../../models/zona';

@Component({
  selector: 'app-solicitud-servicio',
  imports: [RouterLink],
  templateUrl: './solicitud-servicio.html',
  styleUrl: './solicitud-servicio.css',
})
export class SolicitudServicio implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly categoriaServicioService = inject(CategoriaServicioService);
  private readonly zonaService = inject(ZonaService);
  private readonly solicitudService = inject(SolicitudService);
  private readonly storageService = inject(StorageService);

  readonly loading = signal(false);
  readonly success = signal(false);
  readonly error = signal(false);
  readonly imagenError = signal<string | null>(null);
  readonly advertenciaImagenes = signal<string | null>(null);
  readonly categorias = signal<CategoriaServicio[]>([]);
  readonly zonas = signal<Zona[]>([]);
  readonly tecnicoNombre = signal<string | null>(null);
  readonly tecnicoId = signal<number | null>(null);

  readonly imagenesSeleccionadas = signal<File[]>([]);
  readonly previews = signal<string[]>([]);

  readonly categoria = signal(0);
  readonly zona = signal(0);
  readonly descripcion = signal('');
  readonly fechaTentativa = signal('');
  readonly horarioPreferido = signal('');
  readonly direccion = signal('');

  readonly horarios = ['Mañana (8am-12pm)', 'Tarde (12pm-5pm)', 'Noche (5pm-8pm)'];
  readonly maxImagenes = MAX_SOLICITUD_IMAGES;

  readonly puedeAgregarImagenes = computed(
    () => this.imagenesSeleccionadas().length < MAX_SOLICITUD_IMAGES,
  );

  readonly puedeEnviar = computed(
    () =>
      this.categoria() > 0 &&
      this.zona() > 0 &&
      this.descripcion().trim() !== '' &&
      this.fechaTentativa().trim() !== '' &&
      this.horarioPreferido().trim() !== '' &&
      this.direccion().trim() !== '',
  );

  private readonly selectedCategoriaNombre = computed(() => {
    const id = this.categoria();
    if (id <= 0) return null;
    return this.categorias().find((c) => c.id_categoria === id)?.nombre ?? null;
  });

  ngOnInit(): void {
    this.route.queryParams.subscribe((params) => {
      if (params['tecnicoNombre']) {
        this.tecnicoNombre.set(decodeURIComponent(params['tecnicoNombre']));
      }
      if (params['tecnicoId']) {
        this.tecnicoId.set(Number(params['tecnicoId']));
      }
      if (params['categoriaId']) {
        this.categoria.set(Number(params['categoriaId']));
      }
    });

    this.categoriaServicioService.obtenerCategorias().subscribe({
      next: (cats) => this.categorias.set(cats),
    });
    this.zonaService.obtenerZonas().subscribe({
      next: (zs) => this.zonas.set(zs),
    });
  }

  onDropzoneClick(input: HTMLInputElement): void {
    input.click();
  }

  onFileInputChange(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.addFiles(input.files);
    input.value = '';
  }

  onDropzoneKeydown(event: KeyboardEvent, input: HTMLInputElement): void {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      input.click();
    }
  }

  addFiles(fileList: FileList | null): void {
    if (!fileList) {
      return;
    }

    this.imagenError.set(null);
    const current = [...this.imagenesSeleccionadas()];

    for (const file of Array.from(fileList)) {
      if (current.length >= MAX_SOLICITUD_IMAGES) {
        this.imagenError.set(`Máximo ${MAX_SOLICITUD_IMAGES} imágenes por solicitud.`);
        break;
      }

      const validationError = this.storageService.validateImageFile(file);
      if (validationError) {
        this.imagenError.set(validationError);
        continue;
      }

      current.push(file);
    }

    this.setImagenes(current);
  }

  removeImagen(index: number): void {
    const files = [...this.imagenesSeleccionadas()];
    const previews = [...this.previews()];
    URL.revokeObjectURL(previews[index]);
    files.splice(index, 1);
    previews.splice(index, 1);
    this.imagenesSeleccionadas.set(files);
    this.previews.set(previews);
  }

  async onSubmit(): Promise<void> {
    if (!this.puedeEnviar()) {
      return;
    }

    const categoriaNombre = this.selectedCategoriaNombre();
    this.loading.set(true);
    this.error.set(false);
    this.advertenciaImagenes.set(null);

    const data = {
      id_categoria: this.categoria()!,
      id_zona: this.zona()!,
      titulo: categoriaNombre ?? 'Solicitud de servicio',
      descripcion: this.descripcion(),
      direccion_referencia: this.direccion(),
      id_tecnico: this.tecnicoId() ?? undefined,
    };

    try {
      const result = await firstValueFrom(this.solicitudService.crearSolicitud(data));
      if (result === null) {
        this.loading.set(false);
        this.error.set(true);
        return;
      }

      const uploadErrors = await this.subirImagenes(result.id_solicitud);
      this.loading.set(false);

      if (uploadErrors.length > 0) {
        this.advertenciaImagenes.set(
          `Solicitud creada, pero ${uploadErrors.length} imagen(es) no se pudieron subir.`,
        );
      }

      this.success.set(true);
    } catch {
      this.loading.set(false);
      this.error.set(true);
    }
  }

  private async subirImagenes(idSolicitud: number): Promise<string[]> {
    const errors: string[] = [];

    for (const file of this.imagenesSeleccionadas()) {
      const path = this.storageService.buildSolicitudPath(idSolicitud, file.name);
      const upload = await this.storageService.uploadFile(path, file);

      if ('error' in upload) {
        errors.push(upload.error);
        continue;
      }

      const registro = await firstValueFrom(
        this.solicitudService.registrarImagen(idSolicitud, { imagen_url: upload.path }),
      );

      if (!registro || typeof registro === 'string') {
        await this.storageService.removeFile(upload.path);
        errors.push('No se pudo registrar la imagen en el servidor.');
      }
    }

    return errors;
  }

  private setImagenes(files: File[]): void {
    this.previews().forEach((url) => URL.revokeObjectURL(url));
    this.imagenesSeleccionadas.set(files);
    this.previews.set(files.map((file) => URL.createObjectURL(file)));
  }

  toNumber(value: unknown): number {
    return Number(value);
  }

  getInitials(name: string | null): string {
    if (!name) return '?';
    const parts = name.split(' ');
    return parts.map((p) => p.charAt(0)).join('').slice(0, 2).toUpperCase();
  }

  irAlPanel(): void {
    this.router.navigate(['/panel-cliente']);
  }
}
