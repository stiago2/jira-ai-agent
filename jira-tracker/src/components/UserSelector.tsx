/**
 * Componente para seleccionar usuarios asignables de un proyecto Jira
 */

import React, { useState, useEffect } from 'react';
import { JiraUser } from '../types/user.types';
import { ApiService } from '../services/api.service';
import './UserSelector.css';

interface UserSelectorProps {
  projectKey: string;
  selectedUserId?: string;
  onUserSelect: (userId: string | undefined) => void;
  disabled?: boolean;
  label?: string;
  placeholder?: string;
  allowUnassigned?: boolean;
}

export const UserSelector: React.FC<UserSelectorProps> = ({
  projectKey,
  selectedUserId,
  onUserSelect,
  disabled = false,
  label = 'Asignar a',
  placeholder = 'Selecciona un usuario (opcional)',
  allowUnassigned = true,
}) => {
  const [users, setUsers] = useState<JiraUser[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      if (!projectKey) {
        return;
      }

      setLoading(true);
      setError(null);

      try {
        const fetchedUsers = await ApiService.getProjectUsers(projectKey);
        setUsers(fetchedUsers);
      } catch (err) {
        console.error('Error al obtener usuarios:', err);
        setError('No se pudieron cargar los usuarios');
        setUsers([]);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, [projectKey]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const value = e.target.value;
    onUserSelect(value === '' ? undefined : value);
  };

  return (
    <div className="user-selector">
      {label && (
        <label htmlFor="user-selector-input" className="user-selector__label">
          {label}
        </label>
      )}

      {loading ? (
        <div className="user-selector__loading">
          Cargando usuarios...
        </div>
      ) : error ? (
        <div className="user-selector__error">
          {error}
        </div>
      ) : (
        <select
          id="user-selector-input"
          className="user-selector__select"
          value={selectedUserId || ''}
          onChange={handleChange}
          disabled={disabled || users.length === 0}
        >
          {allowUnassigned && (
            <option value="">
              {placeholder}
            </option>
          )}

          {users.map((user) => (
            <option key={user.account_id} value={user.account_id}>
              {user.display_name}
              {user.email ? ` (${user.email})` : ''}
            </option>
          ))}

          {users.length === 0 && !loading && (
            <option value="" disabled>
              No hay usuarios disponibles
            </option>
          )}
        </select>
      )}

      {users.length > 0 && (
        <small className="user-selector__help-text">
          {users.length} {users.length === 1 ? 'usuario disponible' : 'usuarios disponibles'}
        </small>
      )}
    </div>
  );
};
