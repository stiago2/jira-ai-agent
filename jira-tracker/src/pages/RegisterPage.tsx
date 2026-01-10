/**
 * Página de registro de usuario
 */

import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { AuthServiceError } from '../services/auth.service';
import { RegisterRequest } from '../types/auth.types';
import './Auth.css';

export const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState<RegisterRequest>({
    email: '',
    username: '',
    password: '',
    jira_email: '',
    jira_api_token: '',
    jira_base_url: '',
  });
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Validaciones
    if (formData.password !== confirmPassword) {
      setError('Las contraseñas no coinciden');
      return;
    }

    if (formData.password.length < 8) {
      setError('La contraseña debe tener al menos 8 caracteres');
      return;
    }

    if (!formData.jira_base_url.startsWith('http')) {
      setError('La URL de Jira debe comenzar con http:// o https://');
      return;
    }

    setIsLoading(true);

    try {
      await register(formData);
      navigate('/'); // Redirigir al home después de registro exitoso
    } catch (err) {
      if (err instanceof AuthServiceError) {
        setError(err.message);
      } else {
        setError('Error al registrar usuario. Por favor, intenta de nuevo.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card register-card">
        <h1>Crear Cuenta</h1>
        <p className="auth-subtitle">Jira AI Agent</p>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-section">
            <h3>Información de Cuenta</h3>

            <div className="form-group">
              <label htmlFor="username">Usuario *</label>
              <input
                type="text"
                id="username"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
                disabled={isLoading}
                autoComplete="username"
                placeholder="usuario123"
                minLength={3}
              />
              <small>Mínimo 3 caracteres</small>
            </div>

            <div className="form-group">
              <label htmlFor="email">Email *</label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
                disabled={isLoading}
                autoComplete="email"
                placeholder="tu@email.com"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">Contraseña *</label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={isLoading}
                autoComplete="new-password"
                placeholder="Mínimo 8 caracteres"
                minLength={8}
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Contraseña *</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                disabled={isLoading}
                autoComplete="new-password"
                placeholder="Repite tu contraseña"
              />
            </div>
          </div>

          <div className="form-section">
            <h3>Credenciales de Jira</h3>
            <p className="form-help">
              Estas credenciales se usarán para interactuar con tu instancia de Jira.
            </p>

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
          </div>

          <button
            type="submit"
            className="btn-primary"
            disabled={isLoading}
          >
            {isLoading ? 'Registrando...' : 'Crear Cuenta'}
          </button>
        </form>

        <p className="auth-footer">
          ¿Ya tienes una cuenta?{' '}
          <Link to="/login">Inicia sesión aquí</Link>
        </p>
      </div>
    </div>
  );
};
