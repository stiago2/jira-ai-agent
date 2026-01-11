/**
 * Componente para seleccionar qué subtareas incluir en el workflow
 */

import React, { useState, useRef, useEffect } from 'react';
import { AVAILABLE_SUBTASKS, setAvailableSubtasks } from '../types/subtask.types';
import { SubtaskService } from '../services/subtask.service';
import './SubtaskSelector.css';

interface SubtaskSelectorProps {
  selectedSubtasks: number[];
  onSubtasksChange: (subtaskIds: number[]) => void;
  disabled?: boolean;
  label?: string;
}

export const SubtaskSelector: React.FC<SubtaskSelectorProps> = ({
  selectedSubtasks,
  onSubtasksChange,
  disabled = false,
  label = 'Subtareas a crear',
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Cargar subtareas del usuario al montar el componente
  useEffect(() => {
    const loadSubtasks = async () => {
      try {
        const subtasks = await SubtaskService.getSubtasks();
        setAvailableSubtasks(subtasks);

        // Si no hay subtareas seleccionadas, seleccionar todas por defecto
        if (selectedSubtasks.length === 0 && subtasks.length > 0) {
          onSubtasksChange(subtasks.map(st => st.id));
        }
      } catch (error) {
        console.error('Error loading subtasks:', error);
      } finally {
        setLoading(false);
      }
    };

    loadSubtasks();
  }, []);

  // Cerrar dropdown al hacer click fuera
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = () => {
    if (!disabled) {
      setIsOpen(!isOpen);
    }
  };

  const handleSubtaskToggle = (subtaskId: number) => {
    if (disabled) return;

    if (selectedSubtasks.includes(subtaskId)) {
      // Deseleccionar (pero mantener al menos 1)
      if (selectedSubtasks.length > 1) {
        onSubtasksChange(selectedSubtasks.filter(id => id !== subtaskId));
      }
    } else {
      // Seleccionar
      onSubtasksChange([...selectedSubtasks, subtaskId]);
    }
  };

  const handleSelectAll = () => {
    if (disabled) return;
    onSubtasksChange(AVAILABLE_SUBTASKS.map(st => st.id));
  };

  const handleDeselectAll = () => {
    if (disabled) return;
    // Mantener al menos la primera subtarea seleccionada
    onSubtasksChange([AVAILABLE_SUBTASKS[0].id]);
  };

  const selectedCount = selectedSubtasks.length;
  const totalCount = AVAILABLE_SUBTASKS.length;
  const allSelected = selectedCount === totalCount;

  if (loading) {
    return (
      <div className="subtask-selector">
        {label && (
          <label className="subtask-selector__label">
            {label}
          </label>
        )}
        <div className="subtask-selector__loading">Cargando subtareas...</div>
      </div>
    );
  }

  return (
    <div className="subtask-selector" ref={dropdownRef}>
      {label && (
        <label className="subtask-selector__label">
          {label}
        </label>
      )}

      <button
        type="button"
        className={`subtask-selector__button ${isOpen ? 'subtask-selector__button--open' : ''}`}
        onClick={handleToggle}
        disabled={disabled}
      >
        <span className="subtask-selector__button-text">
          {selectedCount} de {totalCount} subtareas seleccionadas
        </span>
        <span className="subtask-selector__arrow">
          {isOpen ? '▲' : '▼'}
        </span>
      </button>

      {isOpen && (
        <div className="subtask-selector__dropdown">
          <div className="subtask-selector__actions">
            <button
              type="button"
              className="subtask-selector__action-button"
              onClick={handleSelectAll}
              disabled={allSelected}
            >
              Seleccionar todas
            </button>
            <button
              type="button"
              className="subtask-selector__action-button"
              onClick={handleDeselectAll}
              disabled={selectedCount <= 1}
            >
              Limpiar
            </button>
          </div>

          <div className="subtask-selector__list">
            {AVAILABLE_SUBTASKS.map((subtask) => {
              const isSelected = selectedSubtasks.includes(subtask.id);
              const isOnlyOne = selectedCount === 1 && isSelected;

              return (
                <label
                  key={subtask.id}
                  className={`subtask-selector__option ${
                    isSelected ? 'subtask-selector__option--selected' : ''
                  } ${isOnlyOne ? 'subtask-selector__option--disabled' : ''}`}
                >
                  <input
                    type="checkbox"
                    className="subtask-selector__checkbox"
                    checked={isSelected}
                    onChange={() => handleSubtaskToggle(subtask.id)}
                    disabled={isOnlyOne}
                  />
                  <span className="subtask-selector__emoji">{subtask.emoji}</span>
                  <div className="subtask-selector__option-content">
                    <span className="subtask-selector__option-name">{subtask.name}</span>
                    <span className="subtask-selector__option-description">
                      {subtask.description}
                    </span>
                  </div>
                </label>
              );
            })}
          </div>

          <div className="subtask-selector__footer">
            <small className="subtask-selector__help-text">
              Debe haber al menos 1 subtarea seleccionada
            </small>
          </div>
        </div>
      )}
    </div>
  );
};
