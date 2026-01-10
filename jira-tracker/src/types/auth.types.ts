/**
 * Tipos TypeScript para autenticación
 */

/**
 * Usuario autenticado
 */
export interface User {
  id: number;
  email: string;
  username: string;
  jira_email: string | null;
  jira_base_url: string | null;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  last_login: string | null;
}

/**
 * Request para registro de usuario
 */
export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
  jira_email: string;
  jira_api_token: string;
  jira_base_url: string;
}

/**
 * Request para login
 */
export interface LoginRequest {
  username: string;
  password: string;
}

/**
 * Response de login con token JWT
 */
export interface AuthResponse {
  access_token: string;
  token_type: string;
}

/**
 * Contexto de autenticación
 */
export interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}
