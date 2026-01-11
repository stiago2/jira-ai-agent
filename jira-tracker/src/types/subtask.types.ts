/**
 * Tipos y definiciones para las subtareas del workflow
 */

export interface SubtaskDefinition {
  id: number;  // Changed from string to number for DB IDs
  name: string;
  emoji: string;
  description: string;
  labels: string[];
  order?: number;
  created_at?: string;
  updated_at?: string;
}

export interface SubtaskCreateRequest {
  name: string;
  emoji: string;
  description?: string;
  labels: string[];
}

export interface SubtaskUpdateRequest {
  name?: string;
  emoji?: string;
  description?: string;
  labels?: string[];
}

/**
 * Lista de todas las subtareas disponibles (ahora se cargan desde el backend)
 */
export let AVAILABLE_SUBTASKS: SubtaskDefinition[] = [];

export function setAvailableSubtasks(subtasks: SubtaskDefinition[]) {
  AVAILABLE_SUBTASKS = subtasks;
}

/**
 * Subtareas por defecto (todas seleccionadas)
 */
export const getDefaultSubtasks = () => AVAILABLE_SUBTASKS.map(st => st.id);
export const DEFAULT_SUBTASKS: number[] = [];
