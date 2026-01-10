/**
 * Contexto de autenticación para gestión global de estado
 */

import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { User, AuthContextType, RegisterRequest } from '../types/auth.types';
import { AuthService } from '../services/auth.service';

// Crear el contexto
const AuthContext = createContext<AuthContextType | undefined>(undefined);

/**
 * Props del proveedor de autenticación
 */
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Proveedor de autenticación
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Inicializar autenticación desde localStorage al cargar
  useEffect(() => {
    const initAuth = async () => {
      const savedToken = AuthService.getToken();
      const savedUser = AuthService.getUser();

      if (savedToken && savedUser) {
        try {
          // Verificar que el token sigue siendo válido
          const currentUser = await AuthService.getCurrentUser(savedToken);
          setToken(savedToken);
          setUser(currentUser);
          AuthService.saveUser(currentUser); // Actualizar usuario en localStorage
        } catch (error) {
          // Token inválido o expirado, limpiar
          console.error('Token inválido:', error);
          AuthService.clearAuth();
        }
      }

      setIsLoading(false);
    };

    initAuth();
  }, []);

  /**
   * Inicia sesión
   */
  const login = async (username: string, password: string): Promise<void> => {
    try {
      // Obtener token
      const authResponse = await AuthService.login(username, password);
      const newToken = authResponse.access_token;

      // Obtener información del usuario
      const userData = await AuthService.getCurrentUser(newToken);

      // Guardar en estado y localStorage
      setToken(newToken);
      setUser(userData);
      AuthService.saveToken(newToken);
      AuthService.saveUser(userData);
    } catch (error) {
      // Limpiar estado en caso de error
      setToken(null);
      setUser(null);
      AuthService.clearAuth();
      throw error;
    }
  };

  /**
   * Registra un nuevo usuario
   */
  const register = async (data: RegisterRequest): Promise<void> => {
    try {
      // Registrar usuario
      await AuthService.register(data);

      // Hacer login automáticamente después del registro
      await login(data.username, data.password);
    } catch (error) {
      // Limpiar estado en caso de error
      setToken(null);
      setUser(null);
      AuthService.clearAuth();
      throw error;
    }
  };

  /**
   * Cierra sesión
   */
  const logout = (): void => {
    if (token) {
      AuthService.logout(token);
    } else {
      AuthService.clearAuth();
    }

    setToken(null);
    setUser(null);
  };

  /**
   * Refresca la información del usuario actual
   */
  const refreshUser = async (): Promise<void> => {
    if (!token) {
      throw new Error('No hay sesión activa');
    }

    try {
      const userData = await AuthService.getCurrentUser(token);
      setUser(userData);
      AuthService.saveUser(userData);
    } catch (error) {
      // Si falla, probablemente el token expiró
      logout();
      throw error;
    }
  };

  const value: AuthContextType = {
    user,
    token,
    isAuthenticated: !!user && !!token,
    isLoading,
    login,
    register,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook para usar el contexto de autenticación
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error('useAuth debe usarse dentro de un AuthProvider');
  }

  return context;
};
