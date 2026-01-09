/**
 * Tipos relacionados con usuarios de Jira
 */

export interface JiraUser {
  account_id: string;
  display_name: string;
  email?: string;
  active: boolean;
  avatar_url?: string;
}

export interface GetProjectUsersResponse {
  success: boolean;
  project_key: string;
  total_users: number;
  users: JiraUser[];
}
