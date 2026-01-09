/**
 * Tipos relacionados con workflows de contenido de Instagram
 */

export interface SubtaskInfo {
  key: string;
  phase: string;
  emoji: string;
  url: string;
}

export interface CreateInstagramContentRequest {
  text: string;
  description?: string;
  project_key?: string;
}

export interface CreateInstagramContentResponse {
  success: boolean;
  main_task_key: string;
  main_task_url: string;
  content_type: string;
  subtasks: SubtaskInfo[];
  total_tasks: number;
}
