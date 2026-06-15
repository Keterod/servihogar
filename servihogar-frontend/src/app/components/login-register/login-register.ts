import { Component, computed, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { AuthProfile } from '../../models/auth';
import { AuthService } from '../../services/auth.service';

type ModoPantalla = 'login' | 'register';
type RolUsuario = 'cliente' | 'tecnico';

interface FormFields {
  nombre: string;
  email: string;
  password: string;
  confirmPassword: string;
  especialidad: string;
  zona: string;
  telefono: string;
}

@Component({
  selector: 'app-login-register',
  standalone: true,
  imports: [],
  templateUrl: './login-register.html',
  styleUrl: './login-register.css',
})
export class LoginRegister {
  private readonly authService = inject(AuthService);
  private readonly router = inject(Router);

  readonly modo = signal<ModoPantalla>('login');
  readonly rol = signal<RolUsuario>('cliente');
  readonly cargando = signal(false);
  readonly error = signal<string | null>(null);
  readonly mensajePendiente = signal<string | null>(null);

  readonly form = signal<FormFields>({
    nombre: '',
    email: '',
    password: '',
    confirmPassword: '',
    especialidad: '',
    zona: '',
    telefono: '',
  });

  readonly tituloFormulario = computed(() => {
    if (this.modo() === 'login') {
      return this.rol() === 'cliente'
        ? 'Iniciar sesión como cliente'
        : 'Iniciar sesión como técnico';
    }
    return this.rol() === 'cliente' ? 'Crear cuenta de cliente' : 'Crear cuenta de técnico';
  });

  readonly textoBoton = computed(() => {
    if (this.modo() === 'register') {
      return 'Próximamente';
    }
    return this.cargando() ? 'Iniciando sesión...' : 'Iniciar sesión';
  });

  readonly puedeEnviar = computed(() => {
    if (this.cargando()) {
      return false;
    }

    const f = this.form();

    if (this.modo() === 'register') {
      return false;
    }

    return f.email.trim() !== '' && f.password.trim() !== '';
  });

  setModo(modo: ModoPantalla): void {
    this.modo.set(modo);
    this.error.set(null);
    this.mensajePendiente.set(null);
    this.form.set({
      nombre: '',
      email: '',
      password: '',
      confirmPassword: '',
      especialidad: '',
      zona: '',
      telefono: '',
    });
  }

  setRol(rol: RolUsuario): void {
    this.rol.set(rol);
    this.error.set(null);
    this.mensajePendiente.set(null);
  }

  actualizarCampo(campo: keyof FormFields, valor: string): void {
    this.form.update((actual) => ({ ...actual, [campo]: valor }));
  }

  async enviarFormulario(): Promise<void> {
    if (this.modo() === 'register' || !this.puedeEnviar()) {
      return;
    }

    this.cargando.set(true);
    this.error.set(null);
    this.mensajePendiente.set(null);

    const { email, password } = this.form();
    const resultado = await this.authService.login(email, password);

    this.cargando.set(false);

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
