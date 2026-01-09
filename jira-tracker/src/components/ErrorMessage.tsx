/**
 * Componente para mostrar mensajes de error
 */
import React from 'react';
import './ErrorMessage.css';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <div className="error-message">
      <div className="error-message__icon">⚠️</div>
      <p className="error-message__text">{message}</p>
      {onRetry && (
        <button className="error-message__button" onClick={onRetry}>
          Reintentar
        </button>
      )}
    </div>
  );
};
