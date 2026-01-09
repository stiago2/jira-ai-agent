/**
 * Componente para input de texto de tarea
 */
import React, { useState } from 'react';
import './TaskInput.css';

interface TaskInputProps {
  onSubmit: (text: string, description?: string) => void;
  loading?: boolean;
  placeholder?: string;
  buttonText?: string;
}

export const TaskInput: React.FC<TaskInputProps> = ({
  onSubmit,
  loading = false,
  placeholder = 'Describe tu tarea en lenguaje natural...',
  buttonText = 'Crear Tarea',
}) => {
  const [text, setText] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (text.trim() && !loading) {
      onSubmit(text.trim(), description.trim() || undefined);
      setText('');
      setDescription('');
    }
  };

  return (
    <form className="task-input" onSubmit={handleSubmit}>
      <div className="task-input__field-group">
        <label htmlFor="task-text" className="task-input__label">
          Título del contenido: *
        </label>
        <textarea
          id="task-text"
          className="task-input__textarea"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={placeholder}
          disabled={loading}
          rows={3}
          required
        />
      </div>

      <div className="task-input__field-group">
        <label htmlFor="task-description" className="task-input__label">
          Descripción detallada (opcional):
        </label>
        <textarea
          id="task-description"
          className="task-input__textarea task-input__textarea--description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Agrega detalles adicionales sobre el contenido..."
          disabled={loading}
          rows={4}
        />
        <small className="task-input__help-text">
          Información adicional: requisitos, especificaciones, notas, etc.
        </small>
      </div>

      <button
        type="submit"
        className="task-input__button"
        disabled={loading || !text.trim()}
      >
        {loading ? 'Creando...' : buttonText}
      </button>
    </form>
  );
};
