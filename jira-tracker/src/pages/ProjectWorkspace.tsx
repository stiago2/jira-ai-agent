/**
 * Página de workspace del proyecto - Creación de tareas
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ApiService, ApiServiceError } from '../services/api.service';
import { MultiTaskInput } from '../components/MultiTaskInput';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import { BatchResults } from '../components/BatchResults';
import { JiraProject } from '../types/project.types';
import { CreateBatchTasksResponse } from '../types/batch.types';
import './ProjectWorkspace.css';

export const ProjectWorkspace: React.FC = () => {
  const { projectKey } = useParams<{ projectKey: string }>();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [batchResults, setBatchResults] = useState<CreateBatchTasksResponse | null>(null);
  const [projectName, setProjectName] = useState<string>('');
  const [loadingProject, setLoadingProject] = useState(true);

  // Determinar si el proyecto usa workflow de Instagram
  const isInstagramProject = projectKey === 'KAN';

  // Cargar información del proyecto
  useEffect(() => {
    const loadProjectInfo = async () => {
      try {
        const projects = await ApiService.getProjects();
        const currentProject = projects.find((p: JiraProject) => p.key === projectKey);
        if (currentProject) {
          setProjectName(currentProject.name);
        } else {
          setProjectName(projectKey || '');
        }
      } catch (err) {
        // Si falla, usar el project key como nombre
        setProjectName(projectKey || '');
      } finally {
        setLoadingProject(false);
      }
    };

    if (projectKey) {
      loadProjectInfo();
    }
  }, [projectKey]);

  const handleCreateTasks = async (tasks: Array<{ text: string; description?: string }>) => {
    if (!projectKey) return;

    setLoading(true);
    setError(null);
    setBatchResults(null);

    try {
      // Usar endpoint de batch para crear múltiples workflows
      const result: CreateBatchTasksResponse = await ApiService.createBatchTasks({
        tasks: tasks,
        project_key: projectKey,
      });

      setBatchResults(result);
    } catch (err) {
      if (err instanceof ApiServiceError) {
        setError(err.message);
      } else {
        setError('Error al crear los workflows');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  const handleCloseResults = () => {
    setBatchResults(null);
  };

  return (
    <div className="project-workspace">
      <header className="project-workspace__header">
        <button className="project-workspace__back-button" onClick={handleBack}>
          ← Volver
        </button>
        <div className="project-workspace__header-content">
          <h1 className="project-workspace__title">
            {loadingProject ? 'Cargando...' : projectName}
          </h1>
          <p className="project-workspace__subtitle">
            {projectKey && <span className="project-workspace__key">{projectKey}</span>}
            {' · '}
            {isInstagramProject
              ? 'Workflow de contenido Instagram (Reels/Historias)'
              : 'Creación de workflows en batch'}
          </p>
        </div>
      </header>

      <main className="project-workspace__content">
        <div className="project-workspace__form-container">
          {loading && <LoadingSpinner message="Creando workflows..." />}

          {error && !loading && (
            <ErrorMessage message={error} onRetry={() => setError(null)} />
          )}

          {batchResults && !loading && (
            <BatchResults
              results={batchResults}
              onClose={handleCloseResults}
            />
          )}

          {!loading && !batchResults && (
            <MultiTaskInput
              onSubmit={handleCreateTasks}
              loading={loading}
              placeholder={
                isInstagramProject
                  ? 'Ej: Crear reel sobre viaje a Cartagena, alta prioridad'
                  : 'Ej: Corregir bug en login, prioridad alta'
              }
              buttonText={isInstagramProject ? 'Crear Workflows' : 'Crear Tareas'}
              projectKey={projectKey}
              showSubtaskSelector={isInstagramProject}
            />
          )}
        </div>

        <aside className="project-workspace__info">
          <h3 className="project-workspace__info-title">Cómo usar</h3>
          <ul className="project-workspace__info-list">
            <li>Click en "+ Agregar tarea" para más workflows</li>
            <li>Describe cada tarea en lenguaje natural</li>
            <li>Agrega descripción detallada (opcional)</li>
            <li>Especifica prioridad: alta, media, baja</li>
            <li>Selecciona un usuario del menú desplegable</li>
            <li>Agrega etiquetas: "etiquetas: tag1, tag2"</li>
            {isInstagramProject && (
              <>
                <li>Especifica tipo: "reel", "historia" o "carrusel"</li>
                <li>Cada workflow crea 1 tarea + 6 subtareas</li>
              </>
            )}
          </ul>
        </aside>
      </main>
    </div>
  );
};
