/**
 * Tipos relacionados con la creación de tareas simples
 */

export interface CreateTaskRequest {
  text: string;
  project_key: string;
}

export interface CreateTaskResponse {
  success: boolean;
  issue_key: string;
  issue_url: string;
  parsed_data: {
    summary: string;
    description: string;
    issue_type: string;
    priority: string;
    assignee: string | null;
    labels: string[];
    confidence: number;
  };
  confidence: number;
}
