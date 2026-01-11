/**
 * Página principal - Selector de proyectos
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { JiraProject } from '../types/project.types';
import { ApiService, ApiServiceError } from '../services/api.service';
import { ProjectSelector } from '../components/ProjectSelector';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { ErrorMessage } from '../components/ErrorMessage';
import './HomePage.css';

export const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [projects, setProjects] = useState<JiraProject[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

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

  const handleProjectSelect = (projectKey: string) => {
    navigate(`/project/${projectKey}`);
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

  return (
    <div className="home-page">
      <header className="home-page__header">
        <div className="header-content">
          <div>
            <h1 className="home-page__title">Jira AI Agent</h1>
            <p className="home-page__subtitle">
              Crea tareas en Jira usando lenguaje natural
            </p>
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
        </div>
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
