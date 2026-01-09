/**
 * Componente de loading spinner
 */
import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
  message?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({ message }) => {
  return (
    <div className="loading-spinner">
      <div className="loading-spinner__circle"></div>
      {message && <p className="loading-spinner__message">{message}</p>}
    </div>
  );
};
