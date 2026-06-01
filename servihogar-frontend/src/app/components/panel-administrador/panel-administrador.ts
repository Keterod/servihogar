import { Component, computed, signal } from '@angular/core';

type EstadoValidacion = 'pendiente' | 'validado' | 'rechazado';
type RolUsuario = 'cliente' | 'tecnico' | 'administrador';
type EstadoUsuario = 'activo' | 'pendiente' | 'rechazado';

interface TecnicoAdmin {
  id: number;
  nombre: string;
  especialidad: string;
  zona: string;
  estadoValidacion: EstadoValidacion;
  fechaRegistro: string;
}

interface Categoria {
  id: number;
  nombre: string;
  descripcion?: string;
}

interface Usuario {
  id: number;
  nombre: string;
  rol: RolUsuario;
  estado: EstadoUsuario;
}

interface FormCategoria {
  nombre: string;
  descripcion: string;
}

interface Reportes {
  solicitudesPublicadas: number;
  cotizacionesRegistradas: number;
  serviciosFinalizados: number;
}

@Component({
  selector: 'app-panel-administrador',
  imports: [],
  templateUrl: './panel-administrador.html',
  styleUrl: './panel-administrador.css',
})
export class PanelAdministrador {
  readonly tecnicos = signal<TecnicoAdmin[]>([
    {
      id: 1,
      nombre: 'Carlos Mendoza',
      especialidad: 'Gasfitería menor',
      zona: 'Huancayo Centro',
      estadoValidacion: 'validado',
      fechaRegistro: '2026-05-15',
    },
    {
      id: 2,
      nombre: 'Luis Arango',
      especialidad: 'Electricidad básica',
      zona: 'El Tambo',
      estadoValidacion: 'pendiente',
      fechaRegistro: '2026-05-28',
    },
    {
      id: 3,
      nombre: 'Rosa Huamán',
      especialidad: 'Gasfitería menor',
      zona: 'Chilca',
      estadoValidacion: 'pendiente',
      fechaRegistro: '2026-05-30',
    },
    {
      id: 4,
      nombre: 'Pedro Vargas',
      especialidad: 'Pintura básica',
      zona: 'Huancayo Centro',
      estadoValidacion: 'rechazado',
      fechaRegistro: '2026-05-20',
    },
  ]);

  readonly categorias = signal<Categoria[]>([
    { id: 1, nombre: 'Gasfitería menor', descripcion: 'Reparaciones de agua y desagüe' },
    { id: 2, nombre: 'Electricidad básica', descripcion: 'Instalaciones eléctricas menores' },
    {
      id: 3,
      nombre: 'Mantenimiento de PC',
      descripcion: 'Soporte técnico y mantenimiento de equipos',
    },
    { id: 4, nombre: 'Pintura básica', descripcion: 'Pintura interior y exterior' },
    { id: 5, nombre: 'Armado de muebles', descripcion: 'Montaje de muebles y estanterías' },
    { id: 6, nombre: 'Reparaciones menores', descripcion: 'Arreglos generales del hogar' },
  ]);

  readonly usuarios = signal<Usuario[]>([
    { id: 1, nombre: 'Mariana Quispe', rol: 'cliente', estado: 'activo' },
    { id: 2, nombre: 'Carlos Mendoza', rol: 'tecnico', estado: 'activo' },
    { id: 3, nombre: 'Luis Arango', rol: 'tecnico', estado: 'pendiente' },
    { id: 4, nombre: 'Rosa Huamán', rol: 'tecnico', estado: 'pendiente' },
    { id: 5, nombre: 'Administrador Demo', rol: 'administrador', estado: 'activo' },
  ]);

  readonly reportes = signal<Reportes>({
    solicitudesPublicadas: 12,
    cotizacionesRegistradas: 28,
    serviciosFinalizados: 7,
  });

  readonly formCategoria = signal<FormCategoria>({ nombre: '', descripcion: '' });
  readonly mensajeAccion = signal('');
  readonly mensajeCategoria = signal('');

  private nextCategoriaId = 7;

  readonly totalTecnicos = computed(() => this.tecnicos().length);

  readonly tecnicosPendientes = computed(
    () => this.tecnicos().filter((t) => t.estadoValidacion === 'pendiente').length
  );

  readonly tecnicosValidados = computed(
    () => this.tecnicos().filter((t) => t.estadoValidacion === 'validado').length
  );

  readonly tecnicosRechazados = computed(
    () => this.tecnicos().filter((t) => t.estadoValidacion === 'rechazado').length
  );

  readonly totalCategorias = computed(() => this.categorias().length);

  readonly totalUsuarios = computed(() => this.usuarios().length);

  readonly tecnicosActivos = computed(() => this.tecnicosValidados());

  readonly puedeAgregarCategoria = computed(() => {
    const nombre = this.formCategoria().nombre.trim();
    if (!nombre) {
      return false;
    }
    const existe = this.categorias().some(
      (c) => c.nombre.toLowerCase() === nombre.toLowerCase()
    );
    return !existe;
  });

  validarTecnico(id: number): void {
    const tecnico = this.tecnicos().find((t) => t.id === id);
    if (!tecnico || tecnico.estadoValidacion !== 'pendiente') {
      return;
    }

    this.tecnicos.update((lista) =>
      lista.map((t) => (t.id === id ? { ...t, estadoValidacion: 'validado' } : t))
    );
    this.mensajeAccion.set('Técnico validado correctamente');
  }

  rechazarTecnico(id: number): void {
    const tecnico = this.tecnicos().find((t) => t.id === id);
    if (!tecnico || tecnico.estadoValidacion !== 'pendiente') {
      return;
    }

    this.tecnicos.update((lista) =>
      lista.map((t) => (t.id === id ? { ...t, estadoValidacion: 'rechazado' } : t))
    );
    this.mensajeAccion.set('Técnico rechazado correctamente');
  }

  agregarCategoria(): void {
    const form = this.formCategoria();
    const nombre = form.nombre.trim();
    if (!nombre) {
      return;
    }

    const existe = this.categorias().some(
      (c) => c.nombre.toLowerCase() === nombre.toLowerCase()
    );
    if (existe) {
      this.mensajeCategoria.set('Ya existe una categoría con ese nombre.');
      return;
    }

    this.categorias.update((lista) => [
      ...lista,
      {
        id: this.nextCategoriaId++,
        nombre,
        descripcion: form.descripcion.trim() || undefined,
      },
    ]);
    this.formCategoria.set({ nombre: '', descripcion: '' });
    this.mensajeCategoria.set('');
  }

  actualizarNombreCategoria(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.formCategoria.update((form) => ({ ...form, nombre: valor }));
    this.mensajeCategoria.set('');
  }

  actualizarDescripcionCategoria(event: Event): void {
    const valor = (event.target as HTMLInputElement).value;
    this.formCategoria.update((form) => ({ ...form, descripcion: valor }));
  }

  getEstadoValidacionLabel(estado: EstadoValidacion): string {
    const labels: Record<EstadoValidacion, string> = {
      pendiente: 'Pendiente',
      validado: 'Validado',
      rechazado: 'Rechazado',
    };
    return labels[estado];
  }

  getEstadoValidacionClass(estado: EstadoValidacion): string {
    return `badge-validacion badge-${estado}`;
  }

  getRolLabel(rol: RolUsuario): string {
    const labels: Record<RolUsuario, string> = {
      cliente: 'Cliente',
      tecnico: 'Técnico',
      administrador: 'Administrador',
    };
    return labels[rol];
  }

  getEstadoUsuarioLabel(estado: EstadoUsuario): string {
    const labels: Record<EstadoUsuario, string> = {
      activo: 'Activo',
      pendiente: 'Pendiente',
      rechazado: 'Rechazado',
    };
    return labels[estado];
  }
}
