/**
 * Componente para crear múltiples tareas a la vez
 */
import React, { useState } from 'react';
import { UserSelector } from './UserSelector';
import { SubtaskSelector } from './SubtaskSelector';
import { DEFAULT_SUBTASKS } from '../types/subtask.types';
import './MultiTaskInput.css';

interface Task {
  id: string;
  text: string;
  description?: string;
  assignee?: string;
  subtasks?: number[];
}

interface MultiTaskInputProps {
  onSubmit: (tasks: Array<{
    text: string;
    description?: string;
    assignee?: string;
    subtasks?: number[];
  }>) => void;
  loading?: boolean;
  placeholder?: string;
  buttonText?: string;
  projectKey?: string;
  showSubtaskSelector?: boolean;
}

export const MultiTaskInput: React.FC<MultiTaskInputProps> = ({
  onSubmit,
  loading = false,
  placeholder = 'Describe tu tarea en lenguaje natural...',
  buttonText = 'Crear Workflows',
  projectKey,
  showSubtaskSelector = false,
}) => {
  const [tasks, setTasks] = useState<Task[]>([
    { id: '1', text: '', description: '', assignee: undefined, subtasks: DEFAULT_SUBTASKS }
  ]);

  const addTask = () => {
    const newId = (Math.max(...tasks.map(t => parseInt(t.id))) + 1).toString();
    setTasks([...tasks, { id: newId, text: '', description: '', assignee: undefined, subtasks: DEFAULT_SUBTASKS }]);
  };

  const removeTask = (id: string) => {
    if (tasks.length > 1) {
      setTasks(tasks.filter(t => t.id !== id));
    }
  };

  const updateTask = (id: string, field: 'text' | 'description' | 'assignee' | 'subtasks', value: string | string[] | number[] | undefined) => {
    setTasks(tasks.map(t => t.id === id ? { ...t, [field]: value } : t));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validTasks = tasks
      .filter(t => t.text.trim())
      .map(t => ({
        text: t.text.trim(),
        description: t.description?.trim() || undefined,
        assignee: t.assignee || undefined,
        subtasks: t.subtasks || DEFAULT_SUBTASKS
      }));
    if (validTasks.length > 0 && !loading) {
      onSubmit(validTasks);
      // Reset to single empty task after submit
      setTasks([{ id: '1', text: '', description: '', assignee: undefined, subtasks: DEFAULT_SUBTASKS }]);
    }
  };

  const hasValidTasks = tasks.some(t => t.text.trim());

  return (
    <form className="multi-task-input" onSubmit={handleSubmit}>
      <div className="multi-task-input__header">
        <label className="multi-task-input__label">
          Tareas a crear ({tasks.filter(t => t.text.trim()).length}):
        </label>
        <button
          type="button"
          className="multi-task-input__add-button"
          onClick={addTask}
          disabled={loading}
          title="Agregar otra tarea"
        >
          <span className="multi-task-input__plus-icon">+</span>
          Agregar tarea
        </button>
      </div>

      <div className="multi-task-input__tasks">
        {tasks.map((task, index) => (
          <div key={task.id} className="multi-task-input__task-card">
            <div className="multi-task-input__task-header">
              <div className="multi-task-input__task-number">{index + 1}</div>
              {tasks.length > 1 && (
                <button
                  type="button"
                  className="multi-task-input__remove-button"
                  onClick={() => removeTask(task.id)}
                  disabled={loading}
                  title="Eliminar tarea"
                >
                  ×
                </button>
              )}
            </div>
            <div className="multi-task-input__task-fields">
              <div className="multi-task-input__field-group">
                <label className="multi-task-input__field-label">
                  Título *
                </label>
                <textarea
                  className="multi-task-input__textarea"
                  value={task.text}
                  onChange={(e) => updateTask(task.id, 'text', e.target.value)}
                  placeholder={placeholder}
                  disabled={loading}
                  rows={2}
                />
              </div>
              <div className="multi-task-input__field-group">
                <label className="multi-task-input__field-label">
                  Descripción (opcional)
                </label>
                <textarea
                  className="multi-task-input__textarea multi-task-input__textarea--description"
                  value={task.description || ''}
                  onChange={(e) => updateTask(task.id, 'description', e.target.value)}
                  placeholder="Detalles adicionales..."
                  disabled={loading}
                  rows={2}
                />
              </div>
              {projectKey && (
                <div className="multi-task-input__field-group">
                  <UserSelector
                    projectKey={projectKey}
                    selectedUserId={task.assignee}
                    onUserSelect={(userId) => updateTask(task.id, 'assignee', userId)}
                    disabled={loading}
                    label="Asignar a (opcional)"
                    placeholder="Sin asignar"
                    allowUnassigned={true}
                  />
                </div>
              )}
              {showSubtaskSelector && (
                <div className="multi-task-input__field-group">
                  <SubtaskSelector
                    selectedSubtasks={task.subtasks || DEFAULT_SUBTASKS}
                    onSubtasksChange={(subtaskIds) => updateTask(task.id, 'subtasks', subtaskIds)}
                    disabled={loading}
                    label="Subtareas a crear"
                  />
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <button
        type="submit"
        className="multi-task-input__submit-button"
        disabled={loading || !hasValidTasks}
      >
        {loading ? 'Creando...' : buttonText}
      </button>
    </form>
  );
};
