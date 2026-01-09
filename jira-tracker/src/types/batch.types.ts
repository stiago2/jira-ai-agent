/**
 * Tipos relacionados con la creación de tareas en batch
 */

import { SubtaskInfo } from './instagram.types';

export interface TaskItem {
  text: string;
  description?: string;
  assignee?: string;
  subtasks?: string[];
}

export interface CreateBatchTasksRequest {
  tasks: TaskItem[];
  project_key: string;
}

export interface TaskResult {
  success: boolean;
  main_task_key?: string;
  main_task_url?: string;
  content_type?: string;
  subtasks?: SubtaskInfo[];
  total_tasks?: number;
  error?: string;
  original_text: string;
}

export interface CreateBatchTasksResponse {
  success: boolean;
  total_requested: number;
  total_created: number;
  total_failed: number;
  total_tasks_created: number;
  results: TaskResult[];
}
