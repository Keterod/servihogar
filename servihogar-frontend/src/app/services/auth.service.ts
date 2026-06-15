import { Injectable, computed, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Session, SupabaseClient, createClient } from '@supabase/supabase-js';
import { Observable, firstValueFrom, of } from 'rxjs';
import { catchError } from 'rxjs/operators';

import { API_BASE_URL } from '../env';
import { AuthProfile, LoginResult } from '../models/auth';
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

  getCurrentUser(): AuthProfile | null {
    return this.profile();
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
}
