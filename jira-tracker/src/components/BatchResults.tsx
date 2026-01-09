/**
 * Componente para mostrar resultados de batch workflows
 */
import React from 'react';
import { CreateBatchTasksResponse } from '../types/batch.types';
import './BatchResults.css';

interface BatchResultsProps {
  results: CreateBatchTasksResponse;
  onClose?: () => void;
}

export const BatchResults: React.FC<BatchResultsProps> = ({ results, onClose }) => {
  const successPercentage = (results.total_created / results.total_requested) * 100;

  return (
    <div className="batch-results">
      <div className="batch-results__header">
        <h3 className="batch-results__title">
          Resultados del Batch
        </h3>
        {onClose && (
          <button className="batch-results__close" onClick={onClose}>
            ×
          </button>
        )}
      </div>

      <div className="batch-results__summary">
        <div className="batch-results__summary-card">
          <div className="batch-results__summary-number">{results.total_requested}</div>
          <div className="batch-results__summary-label">Solicitados</div>
        </div>
        <div className="batch-results__summary-card batch-results__summary-card--success">
          <div className="batch-results__summary-number">{results.total_created}</div>
          <div className="batch-results__summary-label">Exitosos</div>
        </div>
        {results.total_failed > 0 && (
          <div className="batch-results__summary-card batch-results__summary-card--error">
            <div className="batch-results__summary-number">{results.total_failed}</div>
            <div className="batch-results__summary-label">Fallidos</div>
          </div>
        )}
        <div className="batch-results__summary-card batch-results__summary-card--info">
          <div className="batch-results__summary-number">{results.total_tasks_created}</div>
          <div className="batch-results__summary-label">Tareas en Jira</div>
        </div>
      </div>

      <div className="batch-results__progress-bar">
        <div
          className="batch-results__progress-fill"
          style={{ width: `${successPercentage}%` }}
        />
      </div>
      <p className="batch-results__progress-text">
        {successPercentage.toFixed(0)}% de workflows creados exitosamente
      </p>

      <div className="batch-results__items">
        <h4 className="batch-results__items-title">Detalles:</h4>
        {results.results.map((result, index) => (
          <div
            key={index}
            className={`batch-results__item ${result.success ? 'batch-results__item--success' : 'batch-results__item--error'}`}
          >
            <div className="batch-results__item-header">
              <span className="batch-results__item-icon">
                {result.success ? '✅' : '❌'}
              </span>
              <span className="batch-results__item-number">#{index + 1}</span>
              {result.success && result.content_type && (
                <span className="batch-results__item-badge">{result.content_type}</span>
              )}
            </div>

            <p className="batch-results__item-text">{result.original_text}</p>

            {result.success ? (
              <div className="batch-results__item-success">
                <div className="batch-results__item-info">
                  <strong>Tarea principal:</strong> {result.main_task_key}
                </div>
                <a
                  href={result.main_task_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="batch-results__item-link"
                >
                  Ver en Jira →
                </a>
                {result.subtasks && result.subtasks.length > 0 && (
                  <div className="batch-results__item-subtasks">
                    <strong>Subtareas ({result.subtasks.length}):</strong>
                    <div className="batch-results__subtasks-list">
                      {result.subtasks.map((subtask, idx) => (
                        <span key={idx} className="batch-results__subtask" title={subtask.phase}>
                          {subtask.emoji}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="batch-results__item-error">
                <strong>Error:</strong> {result.error}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};
