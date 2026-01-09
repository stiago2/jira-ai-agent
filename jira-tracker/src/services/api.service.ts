/**
 * API Service para comunicación con el backend de Jira AI Agent
 */

import { JiraProject, ProjectsListResponse } from '../types/project.types';
import { CreateTaskRequest, CreateTaskResponse } from '../types/task.types';
import {
  CreateInstagramContentRequest,
  CreateInstagramContentResponse,
} from '../types/instagram.types';
import {
  CreateBatchTasksRequest,
  CreateBatchTasksResponse,
} from '../types/batch.types';
import { JiraUser, GetProjectUsersResponse } from '../types/user.types';
import { ApiError } from '../types/error.types';

// Base URL del backend - puede configurarse via variable de entorno
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Clase para manejo de errores de API
 */
class ApiServiceError extends Error {
  constructor(
    message: string,
    public statusCode?: number,
    public apiError?: ApiError
  ) {
    super(message);
    this.name = 'ApiServiceError';
  }
}

/**
 * Maneja errores de respuesta HTTP
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = `Error HTTP ${response.status}`;
    let apiError: ApiError | undefined;

    try {
      apiError = await response.json();
      if (apiError) {
        errorMessage = apiError.detail || apiError.message || apiError.error || errorMessage;
      }
    } catch {
      // Si no se puede parsear el JSON, usar mensaje por defecto
    }

    throw new ApiServiceError(errorMessage, response.status, apiError);
  }

  return response.json();
}

/**
 * Servicio de API para Jira AI Agent
 */
export class ApiService {
  /**
   * Obtiene la lista de proyectos de Jira
   */
  static async getProjects(): Promise<JiraProject[]> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/projects`);
      const data = await handleResponse<ProjectsListResponse>(response);
      return data.projects;
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al conectar con el servidor');
    }
  }

  /**
   * Crea una tarea simple en Jira
   */
  static async createTask(request: CreateTaskRequest): Promise<CreateTaskResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/tasks/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      return handleResponse<CreateTaskResponse>(response);
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al crear la tarea');
    }
  }

  /**
   * Crea contenido de Instagram (Reel o Historia) con workflow completo
   */
  static async createInstagramContent(
    request: CreateInstagramContentRequest
  ): Promise<CreateInstagramContentResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/content/instagram`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      return handleResponse<CreateInstagramContentResponse>(response);
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al crear contenido de Instagram');
    }
  }

  /**
   * Crea múltiples tareas en batch
   */
  static async createBatchTasks(
    request: CreateBatchTasksRequest
  ): Promise<CreateBatchTasksResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/tasks/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });
      return handleResponse<CreateBatchTasksResponse>(response);
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al crear las tareas en batch');
    }
  }

  /**
   * Obtiene todos los usuarios asignables de un proyecto
   */
  static async getProjectUsers(projectKey: string): Promise<JiraUser[]> {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/projects/${projectKey}/users`
      );
      const data = await handleResponse<GetProjectUsersResponse>(response);
      return data.users;
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al obtener usuarios del proyecto');
    }
  }

  /**
   * Verifica el estado de salud del servidor
   */
  static async healthCheck(): Promise<{ status: string; timestamp: string }> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/health`);
      return handleResponse<{ status: string; timestamp: string }>(response);
    } catch (error) {
      if (error instanceof ApiServiceError) {
        throw error;
      }
      throw new ApiServiceError('Error al verificar el estado del servidor');
    }
  }
}

export { ApiServiceError };
