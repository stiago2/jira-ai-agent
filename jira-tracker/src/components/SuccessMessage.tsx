/**
 * Componente para mostrar mensajes de éxito
 */
import React from 'react';
import './SuccessMessage.css';

interface SuccessMessageProps {
  message: string;
  taskKey?: string;
  taskUrl?: string;
  onClose?: () => void;
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({
  message,
  taskKey,
  taskUrl,
  onClose,
}) => {
  return (
    <div className="success-message">
      <div className="success-message__header">
        <div className="success-message__icon">✅</div>
        <p className="success-message__text">{message}</p>
      </div>
      {taskKey && taskUrl && (
        <a
          href={taskUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="success-message__link"
        >
          Ver tarea {taskKey} en Jira
        </a>
      )}
      {onClose && (
        <button className="success-message__close" onClick={onClose}>
          Cerrar
        </button>
      )}
    </div>
  );
};
