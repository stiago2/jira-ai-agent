/**
 * Tipos relacionados con proyectos de Jira
 */

export interface JiraProject {
  key: string;
  name: string;
  project_type: string;
}

export interface ProjectsListResponse {
  success: boolean;
  total: number;
  projects: JiraProject[];
}
