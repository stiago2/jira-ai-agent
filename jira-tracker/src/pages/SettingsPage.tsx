/**
 * Página de configuración del usuario
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { AuthService, AuthServiceError } from '../services/auth.service';
import { UpdateJiraCredentialsRequest } from '../types/auth.types';
import './Settings.css';

export const SettingsPage: React.FC = () => {
  const { user, token, refreshUser, logout } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState<UpdateJiraCredentialsRequest>({
    jira_email: user?.jira_email || '',
    jira_api_token: '',
    jira_base_url: user?.jira_base_url || '',
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Limpiar mensajes al editar
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validaciones
    if (!formData.jira_base_url.startsWith('http')) {
      setError('La URL de Jira debe comenzar con http:// o https://');
      return;
    }

    if (!formData.jira_email || !formData.jira_api_token || !formData.jira_base_url) {
      setError('Todos los campos son requeridos');
      return;
    }

    setIsLoading(true);

    try {
      await AuthService.updateJiraCredentials(token!, formData);
      await refreshUser();
      setSuccess('Credenciales de Jira actualizadas exitosamente');
      // Limpiar el token del formulario por seguridad
      setFormData({
        ...formData,
        jira_api_token: '',
      });
    } catch (err) {
      if (err instanceof AuthServiceError) {
        setError(err.message);
      } else {
        setError('Error al actualizar credenciales. Por favor, intenta de nuevo.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/');
  };

  const handleLogout = () => {
    setIsMenuOpen(false);
    logout();
    navigate('/login');
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

  const hasJiraCredentials = user?.jira_email && user?.jira_base_url;

  return (
    <div className="settings-container">
      <div className="settings-card">
        <div className="settings-header">
          <div className="settings-header-left">
            <button onClick={handleBack} className="btn-back">
              ← Volver
            </button>
            <h1>Configuración</h1>
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

        <div className="settings-content">
          <div className="user-info-section">
          <h2>Información de Usuario</h2>
          <div className="info-row">
            <span className="info-label">Usuario:</span>
            <span className="info-value">{user?.username}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Email:</span>
            <span className="info-value">{user?.email}</span>
          </div>
          <div className="info-row">
            <span className="info-label">Estado de Jira:</span>
            <span className={`info-value ${hasJiraCredentials ? 'status-active' : 'status-inactive'}`}>
              {hasJiraCredentials ? 'Configurado' : 'No configurado'}
            </span>
          </div>
        </div>

        <div className="jira-config-section">
          <h2>Credenciales de Jira</h2>
          <p className="section-description">
            {hasJiraCredentials
              ? 'Actualiza tus credenciales de Jira si necesitas cambiarlas.'
              : 'Configura tus credenciales de Jira para usar todas las funcionalidades de la aplicación.'}
          </p>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {success && (
            <div className="success-message">
              {success}
            </div>
          )}

          <form onSubmit={handleSubmit} className="settings-form">
            <div className="form-group">
              <label htmlFor="jira_base_url">URL de Jira *</label>
              <input
                type="url"
                id="jira_base_url"
                name="jira_base_url"
                value={formData.jira_base_url}
                onChange={handleChange}
                required
                disabled={isLoading}
                placeholder="https://tuempresa.atlassian.net"
              />
              <small>Ejemplo: https://tuempresa.atlassian.net</small>
            </div>

            <div className="form-group">
              <label htmlFor="jira_email">Email de Jira *</label>
              <input
                type="email"
                id="jira_email"
                name="jira_email"
                value={formData.jira_email}
                onChange={handleChange}
                required
                disabled={isLoading}
                placeholder="tu@empresa.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="jira_api_token">Token API de Jira *</label>
              <input
                type="password"
                id="jira_api_token"
                name="jira_api_token"
                value={formData.jira_api_token}
                onChange={handleChange}
                required
                disabled={isLoading}
                placeholder="ATATT3xFfGF0..."
              />
              <small>
                Genera tu token en:{' '}
                <a
                  href="https://id.atlassian.com/manage-profile/security/api-tokens"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Atlassian API Tokens
                </a>
              </small>
            </div>

            <button
              type="submit"
              className="btn-primary"
              disabled={isLoading}
            >
              {isLoading ? 'Guardando...' : 'Guardar Credenciales'}
            </button>
          </form>
        </div>
        </div>
      </div>
    </div>
  );
};
