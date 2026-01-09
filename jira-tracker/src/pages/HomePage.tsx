/**
 * Página principal - Selector de proyectos
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { JiraProject } from '../types/project.types';
import { ApiService, ApiServiceError } from '../services/api.service';
import { ProjectSelector } from '../components/ProjectSelector';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import './HomePage.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<JiraProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadProjects = async () => {
    setLoading(true);
    setError(null);
    try {
      const projectList = await ApiService.getProjects();
      setProjects(projectList);
    } catch (err) {
      if (err instanceof ApiServiceError) {
        setError(err.message);
      } else {
        setError('Error al cargar los proyectos');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleProjectSelect = (projectKey: string) => {
    navigate(`/project/${projectKey}`);
  };

  return (
    <div className="home-page">
      <header className="home-page__header">
        <h1 className="home-page__title">Jira AI Agent</h1>
        <p className="home-page__subtitle">
          Crea tareas en Jira usando lenguaje natural
        </p>
      </header>

      <main className="home-page__content">
        {loading && <LoadingSpinner message="Cargando proyectos..." />}

        {error && (
          <ErrorMessage
            message={error}
            onRetry={loadProjects}
          />
        )}

        {!loading && !error && (
          <div className="home-page__selector-container">
            <ProjectSelector
              projects={projects}
              selectedProject={null}
              onProjectSelect={handleProjectSelect}
            />
            {projects.length === 0 && (
              <p className="home-page__no-projects">
                No se encontraron proyectos disponibles
              </p>
            )}
          </div>
        )}
      </main>

      <footer className="home-page__footer">
        <p>Conectado al servidor Jira AI Agent</p>
      </footer>
    </div>
  );
};
