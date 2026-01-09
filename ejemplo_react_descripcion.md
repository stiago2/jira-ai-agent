# Cómo usar el campo de descripción desde React

Ahora los endpoints `/api/v1/instagram` y `/api/v1/batch` aceptan un campo opcional `description` para agregar información detallada adicional al contenido.

---

## 📋 Endpoint Individual: `/api/v1/instagram`

### Estructura del Request

```typescript
interface CreateInstagramContentRequest {
  text: string;                // Requerido: Título/resumen del contenido
  description?: string;         // Opcional: Descripción detallada
  project_key?: string;         // Opcional: Default "KAN"
}
```

### Ejemplo 1: Sin descripción (como antes)

```typescript
const response = await fetch('http://localhost:8000/api/v1/instagram', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "Crear carrusel de tips de fotografía en viajes",
    project_key: "KAN"
  })
});

const result = await response.json();
console.log(`Creado: ${result.main_task_key}`);
```

**Resultado en Jira:**
```
Título: 🎠 Carrusel IG | Tips de fotografía en viajes

Descripción:
📹 PROYECTO: Carrusel - Tips de fotografía en viajes

🎯 WORKFLOW DE PRODUCCIÓN:
1. 🎬 Selección de tomas...
```

---

### Ejemplo 2: Con descripción detallada

```typescript
const response = await fetch('http://localhost:8000/api/v1/instagram', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: "Crear carrusel de tips de fotografía en viajes",
    description: `Serie de 10 imágenes con consejos profesionales:
- Tip 1: Regla de los tercios
- Tip 2: Hora dorada
- Tip 3: Composición con líneas
- Tip 4: Uso de reflejos
- Tip 5: Profundidad de campo
Incluir ejemplos visuales de antes/después`,
    project_key: "KAN"
  })
});
```

**Resultado en Jira:**
```
Título: 🎠 Carrusel IG | Tips de fotografía en viajes

Descripción:
📹 PROYECTO: Carrusel - Tips de fotografía en viajes

📝 DESCRIPCIÓN:
Serie de 10 imágenes con consejos profesionales:
- Tip 1: Regla de los tercios
- Tip 2: Hora dorada
- Tip 3: Composición con líneas
- Tip 4: Uso de reflejos
- Tip 5: Profundidad de campo
Incluir ejemplos visuales de antes/después

🎯 WORKFLOW DE PRODUCCIÓN:
1. 🎬 Selección de tomas...
```

---

## 📦 Endpoint Batch: `/api/v1/batch`

### Estructura del Request

```typescript
interface TaskItem {
  text: string;                // Requerido: Título/resumen
  description?: string;         // Opcional: Descripción detallada
}

interface CreateBatchTasksRequest {
  tasks: TaskItem[];           // Array de tareas
  project_key?: string;        // Opcional: Default "KAN"
}
```

### Ejemplo: Batch con descripciones mixtas

```typescript
const response = await fetch('http://localhost:8000/api/v1/batch', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    tasks: [
      {
        text: "Reel sobre tour en Cartagena",
        description: "Recorrido por el centro histórico, Castillo de San Felipe y playas. Duración: 60 seg. Música: upbeat tropical."
      },
      {
        text: "Carrusel de restaurantes en Bogotá",
        // Sin descripción - usará solo el título
      },
      {
        text: "Historia behind the scenes",
        description: "Mostrar el proceso de grabación del reel anterior. Incluir outtakes divertidos."
      }
    ],
    project_key: "KAN"
  })
});

const result = await response.json();
console.log(`Creados: ${result.total_created}/${result.total_requested}`);
```

---

## 🎨 Componente React - Ejemplo completo

```typescript
import React, { useState } from 'react';

interface CreateContentFormProps {
  onSuccess: (taskKey: string) => void;
}

export const CreateContentForm: React.FC<CreateContentFormProps> = ({ onSuccess }) => {
  const [text, setText] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/v1/instagram', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text,
          description: description.trim() || undefined, // Solo enviar si no está vacío
          project_key: 'KAN'
        })
      });

      if (!response.ok) {
        throw new Error('Error al crear contenido');
      }

      const result = await response.json();
      onSuccess(result.main_task_key);

      // Limpiar formulario
      setText('');
      setDescription('');
    } catch (error) {
      console.error('Error:', error);
      alert('Error al crear el contenido');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Campo de título */}
      <div>
        <label htmlFor="text" className="block text-sm font-medium">
          Título del contenido *
        </label>
        <input
          id="text"
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Ej: Crear carrusel de tips de viaje"
          required
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        <p className="mt-1 text-sm text-gray-500">
          Usa lenguaje natural. Puedes incluir: tipo, prioridad, asignado.
        </p>
      </div>

      {/* Campo de descripción (NUEVO) */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Descripción detallada (opcional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Agrega detalles adicionales sobre el contenido..."
          rows={4}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        <p className="mt-1 text-sm text-gray-500">
          Información adicional: requisitos, especificaciones, notas, etc.
        </p>
      </div>

      {/* Botón de submit */}
      <button
        type="submit"
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Creando...' : 'Crear Contenido'}
      </button>
    </form>
  );
};
```

---

## 🔄 Axios - Ejemplo alternativo

```typescript
import axios from 'axios';

// Función helper para crear contenido
export const createInstagramContent = async (
  text: string,
  description?: string
) => {
  const response = await axios.post('http://localhost:8000/api/v1/instagram', {
    text,
    description,
    project_key: 'KAN'
  });

  return response.data;
};

// Uso
const result = await createInstagramContent(
  "Carrusel de mejores hoteles en Medellín",
  "Incluir: precios, ubicación, amenidades principales y tips de reserva"
);

console.log(`Tarea creada: ${result.main_task_key}`);
```

---

## 📱 Fetch con TypeScript completo

```typescript
// types.ts
export interface CreateInstagramContentRequest {
  text: string;
  description?: string;
  project_key?: string;
}

export interface CreateInstagramContentResponse {
  success: boolean;
  main_task_key: string;
  main_task_url: string;
  content_type: 'Reel' | 'Historia' | 'Carrusel';
  subtasks: Array<{
    key: string;
    phase: string;
    emoji: string;
    url: string;
  }>;
  total_tasks: number;
}

// api.ts
export class JiraContentAPI {
  private baseURL = 'http://localhost:8000/api/v1';

  async createContent(
    request: CreateInstagramContentRequest
  ): Promise<CreateInstagramContentResponse> {
    const response = await fetch(`${this.baseURL}/instagram`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al crear contenido');
    }

    return response.json();
  }

  async createBatch(
    tasks: Array<{ text: string; description?: string }>,
    projectKey = 'KAN'
  ) {
    const response = await fetch(`${this.baseURL}/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ tasks, project_key: projectKey })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Error al crear batch');
    }

    return response.json();
  }
}

// Uso
const api = new JiraContentAPI();

const result = await api.createContent({
  text: "Crear reel sobre receta de arepas",
  description: "Mostrar paso a paso la preparación. Duración 60 segundos. Incluir ingredientes en pantalla.",
  project_key: "KAN"
});
```

---

## 🎯 Ventajas del nuevo campo `description`

✅ **Separación clara**: El título es corto y descriptivo, la descripción tiene todos los detalles

✅ **Más flexible**: Puedes agregar toda la información que necesites sin saturar el título

✅ **Mejor organización**: En Jira se ve claramente qué es el proyecto y qué son los detalles

✅ **Opcional**: Si no necesitas descripción, simplemente no la envíes

✅ **Compatible**: Los requests antiguos sin `description` siguen funcionando

---

## 📊 Comparación: Antes vs Ahora

### Antes (solo `text`):
```json
{
  "text": "Crear carrusel de tips de viaje con 10 imágenes, incluir precios, mejores épocas y recomendaciones personales"
}
```
- Título muy largo en Jira
- Difícil de leer
- Todo mezclado

### Ahora (con `description`):
```json
{
  "text": "Crear carrusel de tips de viaje",
  "description": "10 imágenes con:\n- Precios aproximados\n- Mejores épocas\n- Recomendaciones personales"
}
```
- Título conciso: "🎠 Carrusel IG | Tips de viaje"
- Descripción estructurada en la sección correspondiente
- Fácil de leer y mantener
