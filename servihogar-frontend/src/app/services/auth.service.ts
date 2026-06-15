import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, computed, inject, signal } from '@angular/core';
import { Session, SupabaseClient, createClient } from '@supabase/supabase-js';
import { Observable, firstValueFrom, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { AuthProfile, LoginResult, RegisterPayload, RegisterResponse, RegisterResult } from '../models/auth';
import { SUPABASE_ANON_KEY, SUPABASE_URL } from '../supabase.env';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly http = inject(HttpClient);
  private readonly supabase: SupabaseClient;
  private readonly initPromise: Promise<void>;

  private readonly session = signal<Session | null>(null);
  private readonly profile = signal<AuthProfile | null>(null);
  private readonly initialized = signal(false);

  readonly currentUser = this.profile.asReadonly();
  readonly isLoggedIn = computed(() => this.session() !== null);
  readonly displayName = computed(() => {
    const user = this.profile();
    return user ? `${user.nombres} ${user.apellidos}`.trim() : '';
  });

  readonly panelRoute = computed((): string | null => {
    const user = this.profile();
    if (!user) {
      return null;
    }
    if (user.tipo_usuario === 'tecnico' && user.estado_validacion !== 'validado') {
      return null;
    }
    switch (user.tipo_usuario) {
      case 'cliente':
        return '/panel-cliente';
      case 'tecnico':
        return '/panel-tecnico';
      case 'administrador':
        return '/panel-administrador';
      default:
        return null;
    }
  });

  readonly isPendingTechnician = computed(() => {
    const user = this.profile();
    return user?.tipo_usuario === 'tecnico' && user.estado_validacion !== 'validado';
  });

  constructor() {
    this.supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    this.initPromise = this.initialize();

    this.supabase.auth.onAuthStateChange((_event, nextSession) => {
      this.session.set(nextSession);
      if (!nextSession) {
        this.profile.set(null);
      }
    });
  }

  whenReady(): Promise<void> {
    return this.initPromise;
  }

  isAuthenticated(): boolean {
    return this.session() !== null;
  }

  getSession(): Session | null {
    return this.session();
  }

  getSupabase(): SupabaseClient {
    return this.supabase;
  }

  getCurrentUser(): AuthProfile | null {
    return this.profile();
  }

  getAuthHeaders(): { Authorization: string } | null {
    const token = this.session()?.access_token;
    if (!token) {
      return null;
    }
    return { Authorization: `Bearer ${token}` };
  }

  me(): Observable<AuthProfile | null> {
    const token = this.session()?.access_token;
    if (!token) {
      return of(null);
    }

    return this.http
      .get<AuthProfile>(`${API_BASE_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .pipe(catchError(() => of(null)));
  }

  async login(email: string, password: string): Promise<LoginResult> {
    const { data, error } = await this.supabase.auth.signInWithPassword({
      email: email.trim(),
      password,
    });

    if (error || !data.session) {
      return { ok: false, error: 'Correo o contraseña incorrectos.' };
    }

    this.session.set(data.session);
    const profile = await this.fetchMe(data.session.access_token);

    if (!profile) {
      await this.logout();
      return {
        ok: false,
        error: 'Tu cuenta no tiene un perfil de ServiHogar registrado.',
      };
    }

    this.profile.set(profile);

    if (profile.tipo_usuario === 'tecnico' && profile.estado_validacion !== 'validado') {
      return { ok: true, profile, pendingTechnician: true };
    }

    return { ok: true, profile };
  }

  async register(payload: RegisterPayload): Promise<RegisterResult> {
    try {
      const data = await firstValueFrom(
        this.http.post<RegisterResponse>(`${API_BASE_URL}/auth/register`, payload),
      );
      return { ok: true, data };
    } catch (err) {
      return { ok: false, error: this.mapearErrorRegistro(err) };
    }
  }

  async logout(): Promise<void> {
    await this.supabase.auth.signOut();
    this.session.set(null);
    this.profile.set(null);
  }

  private async initialize(): Promise<void> {
    const {
      data: { session },
    } = await this.supabase.auth.getSession();

    this.session.set(session);

    if (session) {
      const profile = await this.fetchMe(session.access_token);
      this.profile.set(profile);
    }

    this.initialized.set(true);
  }

  private fetchMe(token: string): Promise<AuthProfile | null> {
    return firstValueFrom(
      this.http
        .get<AuthProfile>(`${API_BASE_URL}/auth/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        .pipe(catchError(() => of(null))),
    );
  }

  private mapearErrorRegistro(err: unknown): string {
    if (!(err instanceof HttpErrorResponse)) {
      return 'No se pudo completar el registro. Inténtalo nuevamente.';
    }

    const detalle = err.error?.detail;
    if (typeof detalle === 'string' && detalle.trim() !== '') {
      return detalle;
    }

    if (err.status === 409) {
      return 'El correo electrónico ya está registrado.';
    }

    if (err.status === 422) {
      if (Array.isArray(detalle)) {
        return detalle.map((item) => item.msg ?? item).join(' ');
      }
      return 'Revisa los datos del formulario e inténtalo nuevamente.';
    }

    if (err.status === 503) {
      return typeof detalle === 'string' && detalle.trim() !== ''
        ? detalle
        : 'El servicio no está disponible. Inténtalo más tarde.';
    }

    return 'No se pudo completar el registro. Inténtalo nuevamente.';
  }
}
