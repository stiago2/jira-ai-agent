/**
 * Componente para gestionar subtareas personalizadas del usuario
 */

import React, { useState, useEffect } from 'react';
import { SubtaskDefinition, SubtaskCreateRequest } from '../types/subtask.types';
import { SubtaskService, SubtaskServiceError } from '../services/subtask.service';
import './SubtaskManager.css';

interface SubtaskManagerProps {
  onSubtasksChange?: (subtasks: SubtaskDefinition[]) => void;
}

export const SubtaskManager: React.FC<SubtaskManagerProps> = ({ onSubtasksChange }) => {
  const [subtasks, setSubtasks] = useState<SubtaskDefinition[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);

  // Form state
  const [formData, setFormData] = useState<SubtaskCreateRequest>({
    name: '',
    emoji: '📋',
    description: '',
    labels: [],
  });
  const [labelsInput, setLabelsInput] = useState('');

  useEffect(() => {
    loadSubtasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadSubtasks = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await SubtaskService.getSubtasks();
      setSubtasks(data);
      if (onSubtasksChange) {
        onSubtasksChange(data);
      }
    } catch (err) {
      if (err instanceof SubtaskServiceError) {
        setError(err.message);
      } else {
        setError('Error al cargar subtareas');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!formData.name.trim()) {
      setError('El nombre es requerido');
      return;
    }

    try {
      const labels = labelsInput
        .split(',')
        .map(l => l.trim())
        .filter(l => l.length > 0);

      await SubtaskService.createSubtask({
        ...formData,
        labels,
      });

      setSuccess('Subtarea creada exitosamente');
      resetForm();
      await loadSubtasks();
    } catch (err) {
      if (err instanceof SubtaskServiceError) {
        setError(err.message);
      } else {
        setError('Error al crear subtarea');
      }
    }
  };

  const handleUpdate = async (id: number) => {
    setError('');
    setSuccess('');

    try {
      const labels = labelsInput
        .split(',')
        .map(l => l.trim())
        .filter(l => l.length > 0);

      await SubtaskService.updateSubtask(id, {
        ...formData,
        labels,
      });

      setSuccess('Subtarea actualizada exitosamente');
      setEditingId(null);
      resetForm();
      await loadSubtasks();
    } catch (err) {
      if (err instanceof SubtaskServiceError) {
        setError(err.message);
      } else {
        setError('Error al actualizar subtarea');
      }
    }
  };

  const handleDelete = async (id: number) => {
    if (!window.confirm('¿Estás seguro de eliminar esta subtarea?')) {
      return;
    }

    setError('');
    setSuccess('');

    try {
      await SubtaskService.deleteSubtask(id);
      setSuccess('Subtarea eliminada exitosamente');
      await loadSubtasks();
    } catch (err) {
      if (err instanceof SubtaskServiceError) {
        setError(err.message);
      } else {
        setError('Error al eliminar subtarea');
      }
    }
  };

  const startEdit = (subtask: SubtaskDefinition) => {
    setEditingId(subtask.id);
    setFormData({
      name: subtask.name,
      emoji: subtask.emoji,
      description: subtask.description || '',
      labels: subtask.labels,
    });
    setLabelsInput(subtask.labels.join(', '));
    setIsCreating(false);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setIsCreating(false);
    resetForm();
  };

  const resetForm = () => {
    setFormData({
      name: '',
      emoji: '📋',
      description: '',
      labels: [],
    });
    setLabelsInput('');
  };

  if (loading) {
    return <div className="subtask-manager-loading">Cargando subtareas...</div>;
  }

  return (
    <div className="subtask-manager">
      <div className="subtask-manager-header">
        <div>
          <h3>Gestión de Subtareas</h3>
          <p className="subtask-manager-description">
            Personaliza las subtareas que aparecerán en el selector al crear workflows
          </p>
        </div>
        {!isCreating && !editingId && (
          <button
            onClick={() => setIsCreating(true)}
            className="btn-create-subtask"
          >
            + Nueva Subtarea
          </button>
        )}
      </div>

      {error && (
        <div className="subtask-error-message">{error}</div>
      )}

      {success && (
        <div className="subtask-success-message">{success}</div>
      )}

      {(isCreating || editingId) && (
        <form
          onSubmit={editingId ? (e) => { e.preventDefault(); handleUpdate(editingId); } : handleCreate}
          className="subtask-form"
        >
          <div className="subtask-form-row">
            <div className="form-group-small">
              <label>Emoji</label>
              <input
                type="text"
                value={formData.emoji}
                onChange={(e) => setFormData({ ...formData, emoji: e.target.value })}
                maxLength={10}
                required
                placeholder="📋"
              />
            </div>
            <div className="form-group-flex">
              <label>Nombre *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                maxLength={100}
                required
                placeholder="Nombre de la subtarea"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Descripción</label>
            <input
              type="text"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              maxLength={500}
              placeholder="Descripción breve"
            />
          </div>

          <div className="form-group">
            <label>Etiquetas de Jira</label>
            <input
              type="text"
              value={labelsInput}
              onChange={(e) => setLabelsInput(e.target.value)}
              placeholder="etiqueta1, etiqueta2, etiqueta3"
            />
            <small>Separadas por comas</small>
          </div>

          <div className="subtask-form-actions">
            <button type="submit" className="btn-save">
              {editingId ? 'Actualizar' : 'Crear'}
            </button>
            <button type="button" onClick={cancelEdit} className="btn-cancel">
              Cancelar
            </button>
          </div>
        </form>
      )}

      <div className="subtask-list">
        {subtasks.length === 0 ? (
          <div className="subtask-empty">
            No hay subtareas configuradas. Crea tu primera subtarea.
          </div>
        ) : (
          subtasks.map((subtask) => (
            <div key={subtask.id} className="subtask-item">
              <div className="subtask-item-content">
                <div className="subtask-emoji">{subtask.emoji}</div>
                <div className="subtask-info">
                  <div className="subtask-name">{subtask.name}</div>
                  {subtask.description && (
                    <div className="subtask-description">{subtask.description}</div>
                  )}
                  {subtask.labels && subtask.labels.length > 0 && (
                    <div className="subtask-labels">
                      {subtask.labels.map((label, idx) => (
                        <span key={idx} className="subtask-label">{label}</span>
                      ))}
                    </div>
                  )}
                </div>
              </div>
              <div className="subtask-actions">
                <button
                  onClick={() => startEdit(subtask)}
                  className="btn-edit"
                  title="Editar"
                >
                  ✏️
                </button>
                <button
                  onClick={() => handleDelete(subtask.id)}
                  className="btn-delete"
                  title="Eliminar"
                  disabled={subtasks.length <= 1}
                >
                  🗑️
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
