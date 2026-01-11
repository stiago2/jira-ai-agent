/**
 * Página de workspace del proyecto - Creación de tareas
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
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
  const { user, logout } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [batchResults, setBatchResults] = useState<CreateBatchTasksResponse | null>(null);
  const [projectName, setProjectName] = useState<string>('');
  const [loadingProject, setLoadingProject] = useState(true);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

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

  const handleLogout = () => {
    setIsMenuOpen(false);
    logout();
    navigate('/login');
  };

  const handleSettings = () => {
    setIsMenuOpen(false);
    navigate('/settings');
  };

  const handleSubtasks = () => {
    setIsMenuOpen(false);
    navigate('/subtasks');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  // Cerrar el menú cuando se hace clic fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as HTMLElement;
      if (isMenuOpen && !target.closest('.user-menu')) {
        setIsMenuOpen(false);
      }
    };

    if (isMenuOpen) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [isMenuOpen]);

  return (
    <div className="project-workspace">
      <div className="project-workspace__card">
        <header className="project-workspace__header">
          <div className="header-left">
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
          </div>

          <div className="header-user">
            <div className="user-menu">
              <button onClick={toggleMenu} className="user-menu-button">
                <div className="user-avatar">
                  {user?.username.charAt(0).toUpperCase()}
                </div>
                <span className="user-name">{user?.username}</span>
                <svg
                  className={`dropdown-arrow ${isMenuOpen ? 'open' : ''}`}
                  width="12"
                  height="12"
                  viewBox="0 0 12 12"
                  fill="none"
                >
                  <path d="M2 4L6 8L10 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
                </svg>
              </button>

              {isMenuOpen && (
                <div className="user-menu-dropdown">
                  <div className="menu-header">
                    <div className="menu-user-info">
                      <div className="menu-username">{user?.username}</div>
                      <div className="menu-email">{user?.email}</div>
                    </div>
                  </div>
                  <div className="menu-divider"></div>
                  <button onClick={handleSubtasks} className="menu-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M2 4h12M2 8h12M2 12h12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                    </svg>
                    Subtareas
                  </button>
                  <button onClick={handleSettings} className="menu-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M8 10C9.10457 10 10 9.10457 10 8C10 6.89543 9.10457 6 8 6C6.89543 6 6 6.89543 6 8C6 9.10457 6.89543 10 8 10Z" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M13 8C13 8.34 12.98 8.67 12.94 9L14.46 10.18C14.6 10.3 14.64 10.5 14.54 10.68L13.14 13.32C13.04 13.5 12.84 13.56 12.64 13.5L10.81 12.79C10.39 13.12 9.93 13.39 9.43 13.59L9.15 15.54C9.12 15.74 8.95 15.89 8.75 15.89H5.95C5.75 15.89 5.58 15.74 5.55 15.54L5.27 13.59C4.77 13.39 4.31 13.12 3.89 12.79L2.06 13.5C1.86 13.56 1.66 13.5 1.56 13.32L0.16 10.68C0.06 10.5 0.1 10.3 0.24 10.18L1.76 9C1.72 8.67 1.7 8.34 1.7 8C1.7 7.66 1.72 7.33 1.76 7L0.24 5.82C0.1 5.7 0.06 5.5 0.16 5.32L1.56 2.68C1.66 2.5 1.86 2.44 2.06 2.5L3.89 3.21C4.31 2.88 4.77 2.61 5.27 2.41L5.55 0.46C5.58 0.26 5.75 0.11 5.95 0.11H8.75C8.95 0.11 9.12 0.26 9.15 0.46L9.43 2.41C9.93 2.61 10.39 2.88 10.81 3.21L12.64 2.5C12.84 2.44 13.04 2.5 13.14 2.68L14.54 5.32C14.64 5.5 14.6 5.7 14.46 5.82L12.94 7C12.98 7.33 13 7.66 13 8Z" stroke="currentColor" strokeWidth="1.5"/>
                    </svg>
                    Configuración
                  </button>
                  <button onClick={handleLogout} className="menu-item logout">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M6 14H3C2.44772 14 2 13.5523 2 13V3C2 2.44772 2.44772 2 3 2H6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                      <path d="M11 11L14 8M14 8L11 5M14 8H6" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Cerrar Sesión
                  </button>
                </div>
              )}
            </div>
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
    </div>
  );
};
