/**
 * Servicio para gestionar subtareas personalizadas del usuario
 */

import {
  SubtaskDefinition,
  SubtaskCreateRequest,
  SubtaskUpdateRequest,
} from '../types/subtask.types';
import { AuthService } from './auth.service';

// Base URL del backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Clase de error para el servicio de subtareas
 */
export class SubtaskServiceError extends Error {
  constructor(
    message: string,
    public statusCode?: number
  ) {
    super(message);
    this.name = 'SubtaskServiceError';
  }
}

/**
 * Servicio de subtareas
 */
export class SubtaskService {
  /**
   * Obtiene todas las subtareas del usuario actual
   */
  static async getSubtasks(): Promise<SubtaskDefinition[]> {
    try {
      const token = AuthService.getToken();
      if (!token) {
        throw new SubtaskServiceError('No hay sesión activa', 401);
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/subtasks`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new SubtaskServiceError(
          error.detail || 'Error al obtener subtareas',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof SubtaskServiceError) {
        throw error;
      }
      throw new SubtaskServiceError('Error de conexión al obtener subtareas');
    }
  }

  /**
   * Crea una nueva subtarea
   */
  static async createSubtask(data: SubtaskCreateRequest): Promise<SubtaskDefinition> {
    try {
      const token = AuthService.getToken();
      if (!token) {
        throw new SubtaskServiceError('No hay sesión activa', 401);
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/subtasks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new SubtaskServiceError(
          error.detail || 'Error al crear subtarea',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof SubtaskServiceError) {
        throw error;
      }
      throw new SubtaskServiceError('Error de conexión al crear subtarea');
    }
  }

  /**
   * Actualiza una subtarea existente
   */
  static async updateSubtask(
    id: number,
    data: SubtaskUpdateRequest
  ): Promise<SubtaskDefinition> {
    try {
      const token = AuthService.getToken();
      if (!token) {
        throw new SubtaskServiceError('No hay sesión activa', 401);
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/subtasks/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new SubtaskServiceError(
          error.detail || 'Error al actualizar subtarea',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof SubtaskServiceError) {
        throw error;
      }
      throw new SubtaskServiceError('Error de conexión al actualizar subtarea');
    }
  }

  /**
   * Elimina una subtarea
   */
  static async deleteSubtask(id: number): Promise<void> {
    try {
      const token = AuthService.getToken();
      if (!token) {
        throw new SubtaskServiceError('No hay sesión activa', 401);
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/subtasks/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json();
        throw new SubtaskServiceError(
          error.detail || 'Error al eliminar subtarea',
          response.status
        );
      }
    } catch (error) {
      if (error instanceof SubtaskServiceError) {
        throw error;
      }
      throw new SubtaskServiceError('Error de conexión al eliminar subtarea');
    }
  }

  /**
   * Reordena las subtareas
   */
  static async reorderSubtasks(subtaskIds: number[]): Promise<SubtaskDefinition[]> {
    try {
      const token = AuthService.getToken();
      if (!token) {
        throw new SubtaskServiceError('No hay sesión activa', 401);
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/subtasks/reorder`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ subtask_ids: subtaskIds }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new SubtaskServiceError(
          error.detail || 'Error al reordenar subtareas',
          response.status
        );
      }

      return response.json();
    } catch (error) {
      if (error instanceof SubtaskServiceError) {
        throw error;
      }
      throw new SubtaskServiceError('Error de conexión al reordenar subtareas');
    }
  }
}
