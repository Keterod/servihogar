import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { email, form, FormField, minLength, required, submit, validate } from '@angular/forms/signals';
import { ActivatedRoute, Router } from '@angular/router';
import { forkJoin, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { AuthProfile } from '../../models/auth';
import { CategoriaServicio } from '../../models/categoria-servicio';
import { Zona } from '../../models/zona';
import { AuthService } from '../../services/auth.service';
import { CategoriaServicioService } from '../../services/categoria-servicio.service';
import { ZonaService } from '../../services/zona.service';

type ModoPantalla = 'login' | 'register';
type RolUsuario = 'cliente' | 'tecnico';

interface LoginFormModel {
  email: string;
  password: string;
}

interface RegisterFormModel {
  nombres: string;
  apellidos: string;
  email: string;
  password: string;
  telefono: string;
  tipoUsuario: RolUsuario;
  descripcion: string;
  experienciaAnios: number;
  idCategorias: number[];
  idZonas: number[];
}

const LOGIN_MODEL_INICIAL: LoginFormModel = {
  email: '',
  password: '',
};

const REGISTER_MODEL_INICIAL: RegisterFormModel = {
  nombres: '',
  apellidos: '',
  email: '',
  password: '',
  telefono: '',
  tipoUsuario: 'cliente',
  descripcion: '',
  experienciaAnios: 0,
  idCategorias: [],
  idZonas: [],
};

@Component({
  selector: 'app-login-register',
  standalone: true,
  imports: [FormField],
  templateUrl: './login-register.html',
  styleUrl: './login-register.css',
})
export class LoginRegister implements OnInit {
  private readonly authService = inject(AuthService);
  private readonly categoriaService = inject(CategoriaServicioService);
  private readonly zonaService = inject(ZonaService);
  private readonly router = inject(Router);
  private readonly route = inject(ActivatedRoute);

  readonly modo = signal<ModoPantalla>('login');
  readonly error = signal<string | null>(null);
  readonly success = signal<string | null>(null);
  readonly mensajePendiente = signal<string | null>(null);

  readonly loginModel = signal<LoginFormModel>({ ...LOGIN_MODEL_INICIAL });
  readonly registerModel = signal<RegisterFormModel>({ ...REGISTER_MODEL_INICIAL });

  readonly loginForm = form(this.loginModel, (s) => {
    required(s.email, { message: 'El correo es obligatorio' });
    email(s.email, { message: 'Ingresa un correo válido' });
    required(s.password, { message: 'La contraseña es obligatoria' });
    minLength(s.password, 6, { message: 'Mínimo 6 caracteres' });
  });

  readonly registerForm = form(this.registerModel, (s) => {
    required(s.nombres, { message: 'Los nombres son obligatorios' });
    required(s.apellidos, { message: 'Los apellidos son obligatorios' });
    required(s.email, { message: 'El correo es obligatorio' });
    email(s.email, { message: 'Ingresa un correo válido' });
    required(s.password, { message: 'La contraseña es obligatoria' });
    minLength(s.password, 6, { message: 'Mínimo 6 caracteres' });
    required(s.descripcion, {
      message: 'La descripción es obligatoria para técnicos',
      when: ({ valueOf }) => valueOf(s.tipoUsuario) === 'tecnico',
    });
    validate(s.experienciaAnios, ({ value, valueOf }) => {
      if (valueOf(s.tipoUsuario) !== 'tecnico') {
        return undefined;
      }
      if (value() < 0) {
        return { kind: 'min', message: 'Los años de experiencia no pueden ser negativos' };
      }
      return undefined;
    });
  });

  readonly catalogoCategorias = signal<CategoriaServicio[]>([]);
  readonly catalogoZonas = signal<Zona[]>([]);

  readonly tituloEncabezado = computed(() =>
    this.modo() === 'login' ? 'Iniciar sesión' : 'Crear cuenta',
  );

  readonly subtituloEncabezado = computed(() =>
    this.modo() === 'login'
      ? 'Ingresa tu correo y contraseña para acceder a tu panel.'
      : 'Completa tus datos para registrarte en ServiHogar.',
  );

  readonly esTecnico = computed(() => this.registerModel().tipoUsuario === 'tecnico');

  readonly loginTextoBoton = computed(() =>
    this.loginForm().submitting() ? 'Iniciando sesión...' : 'Iniciar sesión',
  );

  readonly registerTextoBoton = computed(() =>
    this.registerForm().submitting() ? 'Creando cuenta...' : 'Registrarse',
  );

  ngOnInit(): void {
    const tab = this.route.snapshot.queryParamMap.get('tab');
    if (tab === 'register') {
      this.setModo('register');
    }

    forkJoin({
      categorias: this.categoriaService.obtenerCategorias().pipe(catchError(() => of([]))),
      zonas: this.zonaService.obtenerZonas().pipe(catchError(() => of([]))),
    }).subscribe(({ categorias, zonas }) => {
      this.catalogoCategorias.set(categorias);
      this.catalogoZonas.set(zonas);
    });
  }

  setModo(modo: ModoPantalla): void {
    this.modo.set(modo);
    this.error.set(null);
    this.success.set(null);
    this.mensajePendiente.set(null);

    if (modo === 'login') {
      this.loginModel.set({ ...LOGIN_MODEL_INICIAL });
    } else {
      this.registerModel.set({ ...REGISTER_MODEL_INICIAL });
    }
  }

  setRol(rol: RolUsuario): void {
    this.registerModel.update((actual) => ({
      ...actual,
      tipoUsuario: rol,
      ...(rol === 'cliente'
        ? { descripcion: '', experienciaAnios: 0, idCategorias: [], idZonas: [] }
        : {}),
    }));
    this.error.set(null);
    this.success.set(null);
    this.mensajePendiente.set(null);
  }

  alternarCategoria(idCategoria: number, seleccionado: boolean): void {
    this.registerModel.update((actual) => ({
      ...actual,
      idCategorias: seleccionado
        ? [...actual.idCategorias, idCategoria]
        : actual.idCategorias.filter((item) => item !== idCategoria),
    }));
  }

  alternarZona(idZona: number, seleccionado: boolean): void {
    this.registerModel.update((actual) => ({
      ...actual,
      idZonas: seleccionado
        ? [...actual.idZonas, idZona]
        : actual.idZonas.filter((item) => item !== idZona),
    }));
  }

  idCategoria(cat: CategoriaServicio): number {
    return cat.id_categoria;
  }

  idZona(zona: Zona): number {
    return zona.id_zona;
  }

  categoriaMarcada(idCategoria: number): boolean {
    return this.registerModel().idCategorias.includes(idCategoria);
  }

  zonaMarcada(idZona: number): boolean {
    return this.registerModel().idZonas.includes(idZona);
  }

  onLoginSubmit(event: Event): void {
    event.preventDefault();
    submit(this.loginForm, async () => {
      await this.procesarLogin();
    });
  }

  onRegisterSubmit(event: Event): void {
    event.preventDefault();
    submit(this.registerForm, async () => {
      await this.procesarRegistro();
    });
  }

  private async procesarLogin(): Promise<void> {
    this.error.set(null);
    this.success.set(null);
    this.mensajePendiente.set(null);

    const { email, password } = this.loginModel();
    const resultado = await this.authService.login(email, password);

    if (!resultado.ok || !resultado.profile) {
      this.error.set(resultado.error ?? 'No se pudo iniciar sesión. Inténtalo nuevamente.');
      return;
    }

    if (resultado.pendingTechnician) {
      this.mensajePendiente.set(
        'Tu cuenta de técnico está pendiente de validación administrativa. No puedes acceder al panel técnico todavía.',
      );
      return;
    }

    this.router.navigateByUrl(this.rutaPorPerfil(resultado.profile));
  }

  private async procesarRegistro(): Promise<void> {
    this.error.set(null);
    this.success.set(null);
    this.mensajePendiente.set(null);

    const form = this.registerModel();
    const payload = {
      nombres: form.nombres.trim(),
      apellidos: form.apellidos.trim(),
      email: form.email.trim(),
      password: form.password,
      tipo_usuario: form.tipoUsuario,
      telefono: form.telefono.trim() || null,
      descripcion: form.tipoUsuario === 'tecnico' ? form.descripcion.trim() : null,
      experiencia_anios: form.tipoUsuario === 'tecnico' ? form.experienciaAnios : null,
      id_categorias: form.tipoUsuario === 'tecnico' ? form.idCategorias : [],
      id_zonas: form.tipoUsuario === 'tecnico' ? form.idZonas : [],
    };

    const resultado = await this.authService.register(payload);

    if (!resultado.ok || !resultado.data) {
      this.error.set(resultado.error ?? 'No se pudo completar el registro.');
      return;
    }

    if (resultado.data.tipo_usuario === 'cliente') {
      this.success.set(resultado.data.mensaje);
      const login = await this.authService.login(form.email, form.password);
      if (login.ok && login.profile && !login.pendingTechnician) {
        this.router.navigateByUrl(this.rutaPorPerfil(login.profile));
        return;
      }
      this.modo.set('login');
      this.loginModel.set({ email: form.email.trim(), password: '' });
      this.registerModel.set({ ...REGISTER_MODEL_INICIAL });
      return;
    }

    this.success.set(resultado.data.mensaje);
    this.mensajePendiente.set(resultado.data.mensaje);
    this.modo.set('login');
    this.loginModel.set({ email: form.email.trim(), password: '' });
    this.registerModel.set({ ...REGISTER_MODEL_INICIAL });
  }

  private rutaPorPerfil(profile: AuthProfile): string {
    switch (profile.tipo_usuario) {
      case 'cliente':
        return '/panel-cliente';
      case 'tecnico':
        return '/panel-tecnico';
      case 'administrador':
        return '/panel-administrador';
      default:
        return '/inicio';
    }
  }
}
