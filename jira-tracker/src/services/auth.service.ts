/**
 * Servicio de autenticación para comunicación con el backend
 */

import {
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
} from '../types/auth.types';

// Base URL del backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Keys para localStorage
const TOKEN_KEY = 'jira_agent_token';
const USER_KEY = 'jira_agent_user';

/**
 * Clase de error para autenticación
 */
export class AuthServiceError extends Error {
  constructor(
    message: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = 'AuthServiceError';
  }
}

/**
 * Servicio de autenticación
 */
export class AuthService {
  /**
   * Registra un nuevo usuario
   */
  static async register(data: RegisterRequest): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new AuthServiceError(
          error.detail || 'Error al registrar usuario',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof AuthServiceError) {
        throw error;
      }
      throw new AuthServiceError('Error de conexión al registrar usuario');
    }
  }

  /**
   * Inicia sesión con usuario y contraseña
   */
  static async login(username: string, password: string): Promise<AuthResponse> {
    try {
      // Crear FormData para OAuth2PasswordRequestForm
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        throw new AuthServiceError(
          error.detail || 'Credenciales incorrectas',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof AuthServiceError) {
        throw error;
      }
      throw new AuthServiceError('Error de conexión al iniciar sesión');
    }
  }

  /**
   * Obtiene la información del usuario actual
   */
  static async getCurrentUser(token: string): Promise<User> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new AuthServiceError(
          error.detail || 'Error al obtener usuario',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof AuthServiceError) {
        throw error;
      }
      throw new AuthServiceError('Error de conexión al obtener usuario');
    }
  }

  /**
   * Cierra sesión (client-side, JWT es stateless)
   */
  static async logout(token: string): Promise<void> {
    try {
      // Llamar al endpoint de logout (opcional, solo para consistency)
      await fetch(`${API_BASE_URL}/api/v1/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    } catch (error) {
      // Ignorar errores de logout
      console.error('Error al hacer logout en el servidor:', error);
    } finally {
      // Siempre limpiar el localStorage
      this.clearAuth();
    }
  }

  /**
   * Guarda el token en localStorage
   */
  static saveToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token);
  }

  /**
   * Obtiene el token de localStorage
   */
  static getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  /**
   * Guarda el usuario en localStorage
   */
  static saveUser(user: User): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
  }

  /**
   * Obtiene el usuario de localStorage
   */
  static getUser(): User | null {
    const userStr = localStorage.getItem(USER_KEY);
    if (!userStr) return null;

    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  }

  /**
   * Limpia la autenticación del localStorage
   */
  static clearAuth(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  /**
   * Verifica si hay un token guardado
   */
  static hasToken(): boolean {
    return !!this.getToken();
  }
}
