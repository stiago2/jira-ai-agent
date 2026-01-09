/**
 * Tipos y definiciones para las subtareas del workflow
 */

export interface SubtaskDefinition {
  id: string;
  name: string;
  emoji: string;
  description: string;
  labels: string[];
}

/**
 * Lista de todas las subtareas disponibles para workflows de Instagram
 */
export const AVAILABLE_SUBTASKS: SubtaskDefinition[] = [
  {
    id: 'seleccion',
    name: 'Selección de tomas',
    emoji: '🎬',
    description: 'Organización del material',
    labels: ['seleccion', 'footage', 'produccion']
  },
  {
    id: 'edicion',
    name: 'Edición',
    emoji: '✂️',
    description: 'Montaje del video',
    labels: ['edicion', 'video-editing', 'postproduccion']
  },
  {
    id: 'audio',
    name: 'Diseño sonoro',
    emoji: '🎵',
    description: 'Audio y música',
    labels: ['audio', 'sound-design', 'postproduccion']
  },
  {
    id: 'color',
    name: 'Color',
    emoji: '🎨',
    description: 'Corrección y gradación de color',
    labels: ['color', 'color-grading', 'postproduccion']
  },
  {
    id: 'copy',
    name: 'Copy / Caption',
    emoji: '✍️',
    description: 'Redacción de texto',
    labels: ['copy', 'caption', 'contenido']
  },
  {
    id: 'export',
    name: 'Export',
    emoji: '📤',
    description: 'Exportación final',
    labels: ['export', 'final', 'delivery']
  }
];

/**
 * Subtareas por defecto (todas seleccionadas)
 */
export const DEFAULT_SUBTASKS = AVAILABLE_SUBTASKS.map(st => st.id);
