/**
 * Componente selector de proyectos de Jira
 */
import React from 'react';
import { JiraProject } from '../types/project.types';
import './ProjectSelector.css';

interface ProjectSelectorProps {
  projects: JiraProject[];
  selectedProject: string | null;
  onProjectSelect: (projectKey: string) => void;
  loading?: boolean;
}

export const ProjectSelector: React.FC<ProjectSelectorProps> = ({
  projects,
  selectedProject,
  onProjectSelect,
  loading = false,
}) => {
  return (
    <div className="project-selector">
      <label htmlFor="project-select" className="project-selector__label">
        Selecciona un proyecto:
      </label>
      <select
        id="project-select"
        className="project-selector__select"
        value={selectedProject || ''}
        onChange={(e) => onProjectSelect(e.target.value)}
        disabled={loading || projects.length === 0}
      >
        <option value="" disabled>
          {loading ? 'Cargando proyectos...' : 'Selecciona un proyecto'}
        </option>
        {projects.map((project) => (
          <option key={project.key} value={project.key}>
            {project.key} - {project.name}
          </option>
        ))}
      </select>
    </div>
  );
};
