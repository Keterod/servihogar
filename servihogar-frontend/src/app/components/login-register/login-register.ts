import { Component, computed, signal } from '@angular/core';

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
  imports: [],
  templateUrl: './login-register.html',
  styleUrl: './login-register.css',
})
export class LoginRegister {
  readonly modo = signal<ModoPantalla>('login');
  readonly rol = signal<RolUsuario>('cliente');

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

  readonly textoBoton = computed(() =>
    this.modo() === 'login' ? 'Iniciar sesión' : 'Crear cuenta'
  );

  readonly puedeEnviar = computed(() => {
    const f = this.form();
    if (this.modo() === 'login') {
      return f.email.trim() !== '' && f.password.trim() !== '';
    }
    return (
      f.nombre.trim() !== '' &&
      f.email.trim() !== '' &&
      f.password.trim() !== '' &&
      f.confirmPassword.trim() !== '' &&
      f.password === f.confirmPassword
    );
  });

  setModo(modo: ModoPantalla): void {
    this.modo.set(modo);
    this.form.set({ nombre: '', email: '', password: '', confirmPassword: '', especialidad: '', zona: '', telefono: '' });
  }

  setRol(rol: RolUsuario): void {
    this.rol.set(rol);
  }

  actualizarCampo(campo: keyof FormFields, valor: string): void {
    this.form.update((actual) => ({ ...actual, [campo]: valor }));
  }
}
