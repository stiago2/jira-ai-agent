/**
 * Página dedicada a la gestión de subtareas personalizadas
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { SubtaskManager } from '../components/SubtaskManager';
import './SubtasksPage.css';

export const SubtasksPage: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleBack = () => {
    navigate('/');
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
    <div className="subtasks-page-container">
      <div className="subtasks-page-card">
        <div className="subtasks-page-header">
          <div className="subtasks-header-left">
            <button onClick={handleBack} className="btn-back">
              ← Volver
            </button>
            <h1>Gestión de Subtareas</h1>
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
                  <button onClick={handleSettings} className="menu-item">
                    <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                      <path d="M8 10C9.10457 10 10 9.10457 10 8C10 6.89543 9.10457 6 8 6C6.89543 6 6 6.89543 6 8C6 9.10457 6.89543 10 8 10Z" stroke="currentColor" strokeWidth="1.5"/>
                      <path d="M13 8C13 8.36 12.96 8.71 12.89 9.05L14.3 10.18C14.42 10.28 14.45 10.46 14.37 10.6L13.03 12.9C12.95 13.04 12.78 13.09 12.63 13.04L10.93 12.38C10.58 12.65 10.2 12.88 9.78 13.05L9.5 14.87C9.48 15.03 9.34 15.15 9.18 15.15H6.5C6.34 15.15 6.2 15.03 6.18 14.87L5.9 13.05C5.48 12.88 5.1 12.65 4.75 12.38L3.05 13.04C2.9 13.09 2.73 13.04 2.65 12.9L1.31 10.6C1.23 10.46 1.26 10.28 1.38 10.18L2.79 9.05C2.72 8.71 2.68 8.36 2.68 8C2.68 7.64 2.72 7.29 2.79 6.95L1.38 5.82C1.26 5.72 1.23 5.54 1.31 5.4L2.65 3.1C2.73 2.96 2.9 2.91 3.05 2.96L4.75 3.62C5.1 3.35 5.48 3.12 5.9 2.95L6.18 1.13C6.2 0.97 6.34 0.85 6.5 0.85H9.18C9.34 0.85 9.48 0.97 9.5 1.13L9.78 2.95C10.2 3.12 10.58 3.35 10.93 3.62L12.63 2.96C12.78 2.91 12.95 2.96 13.03 3.1L14.37 5.4C14.45 5.54 14.42 5.72 14.3 5.82L12.89 6.95C12.96 7.29 13 7.64 13 8Z" stroke="currentColor" strokeWidth="1.5"/>
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

        <div className="subtasks-page-content">
          <div className="page-description">
            <p>
              Crea y personaliza tus propias subtareas para usar en tus workflows.
              Estas subtareas aparecerán automáticamente en el selector cuando crees nuevas tareas.
            </p>
          </div>

          <SubtaskManager />
        </div>
      </div>
    </div>
  );
};
