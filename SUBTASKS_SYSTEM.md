# Sistema de Gestión de Subtareas Personalizadas

## Resumen

Se ha implementado un sistema completo de gestión de subtareas personalizadas que permite a los usuarios crear, editar y eliminar sus propias plantillas de subtareas. Estas subtareas aparecen automáticamente en el selector de subtareas al crear workflows.

## Arquitectura

### Backend (FastAPI + SQLAlchemy)

#### Modelo de Base de Datos

**Archivo:** `app/models/subtask.py`

**Tabla:** `subtask_templates`

**Campos:**
- `id` (Integer, Primary Key) - ID único de la subtarea
- `user_id` (Integer, Foreign Key) - Referencia al usuario propietario
- `name` (String 100) - Nombre de la subtarea
- `emoji` (String 10) - Emoji representativo (default: "📋")
- `description` (Text) - Descripción opcional de la subtarea
- `labels` (Text) - Etiquetas de Jira separadas por comas
- `order` (Integer) - Orden de visualización (default: 0)
- `created_at` (DateTime) - Fecha de creación
- `updated_at` (DateTime) - Fecha de última actualización

**Propiedades especiales:**
- `labels_list` - Property que convierte labels (CSV) a lista y viceversa

#### API Endpoints

**Archivo:** `app/api/routes/subtasks.py`

**Endpoints disponibles:**

1. **GET `/api/v1/subtasks`** - Obtener todas las subtareas del usuario
   - Auto-inicializa con 6 subtareas por defecto si el usuario no tiene ninguna
   - Respuesta: Lista de subtareas ordenadas por campo `order`

2. **POST `/api/v1/subtasks`** - Crear nueva subtarea
   - Body: `{ name, emoji, description?, labels[] }`
   - Añade la subtarea al final del listado actual
   - Respuesta: Subtarea creada con ID asignado

3. **PUT `/api/v1/subtasks/{id}`** - Actualizar subtarea existente
   - Body: `{ name?, emoji?, description?, labels[]? }`
   - Solo actualiza los campos proporcionados
   - Respuesta: Subtarea actualizada

4. **DELETE `/api/v1/subtasks/{id}`** - Eliminar subtarea
   - Validación: No permite eliminar si solo queda 1 subtarea
   - Respuesta: 204 No Content en caso de éxito

5. **POST `/api/v1/subtasks/reorder`** - Reordenar subtareas
   - Body: `{ subtask_ids: [1, 3, 2, 4, ...] }`
   - Actualiza el campo `order` según el índice en el array
   - Respuesta: Lista de subtareas reordenadas

**Subtareas por defecto (auto-inicialización):**

```python
DEFAULT_SUBTASKS_DATA = [
    {
        "name": "Selección de tomas",
        "emoji": "🎬",
        "description": "Organización del material",
        "labels": ["seleccion", "footage", "produccion"],
        "order": 0
    },
    {
        "name": "Edición",
        "emoji": "✂️",
        "description": "Montaje del video",
        "labels": ["edicion", "video-editing", "postproduccion"],
        "order": 1
    },
    {
        "name": "Diseño sonoro",
        "emoji": "🎵",
        "description": "Audio y música",
        "labels": ["audio", "sound-design", "postproduccion"],
        "order": 2
    },
    {
        "name": "Color",
        "emoji": "🎨",
        "description": "Corrección y gradación de color",
        "labels": ["color", "color-grading", "postproduccion"],
        "order": 3
    },
    {
        "name": "Copy / Caption",
        "emoji": "✍️",
        "description": "Redacción de texto",
        "labels": ["copy", "caption", "contenido"],
        "order": 4
    },
    {
        "name": "Export",
        "emoji": "📤",
        "description": "Exportación final",
        "labels": ["export", "final", "delivery"],
        "order": 5
    }
]
```

**Autenticación:**
- Todos los endpoints requieren JWT token en header: `Authorization: Bearer <token>`
- Usa la dependency `get_current_user` para obtener el usuario autenticado
- Las subtareas son privadas por usuario (filtradas por `user_id`)

#### Registro en Main App

**Archivo:** `app/main.py`

```python
from app.api.routes import subtasks

app.include_router(subtasks.router, prefix="/api/v1")
```

### Frontend (React + TypeScript)

#### Tipos

**Archivo:** `src/types/subtask.types.ts`

```typescript
export interface SubtaskDefinition {
  id: number;  // ID numérico de base de datos
  name: string;
  emoji: string;
  description: string;
  labels: string[];
  order?: number;
  created_at?: string;
  updated_at?: string;
}

// Array mutable cargado dinámicamente desde backend
export let AVAILABLE_SUBTASKS: SubtaskDefinition[] = [];

export function setAvailableSubtasks(subtasks: SubtaskDefinition[]) {
  AVAILABLE_SUBTASKS = subtasks;
}
```

**Cambios importantes:**
- IDs cambiaron de `string` a `number` para compatibilidad con base de datos
- `AVAILABLE_SUBTASKS` cambió de `const` a `let` para permitir actualización dinámica
- Se agregó función `setAvailableSubtasks()` para actualizar el array global

#### Servicio de API

**Archivo:** `src/services/subtask.service.ts`

**Métodos disponibles:**

```typescript
class SubtaskService {
  static async getSubtasks(): Promise<SubtaskDefinition[]>
  static async createSubtask(data: SubtaskCreateRequest): Promise<SubtaskDefinition>
  static async updateSubtask(id: number, data: SubtaskUpdateRequest): Promise<SubtaskDefinition>
  static async deleteSubtask(id: number): Promise<void>
  static async reorderSubtasks(subtaskIds: number[]): Promise<SubtaskDefinition[]>
}
```

**Manejo de errores:**
- Clase personalizada `SubtaskServiceError` con mensaje y código de estado
- Validación de token de autenticación antes de cada request
- Parseo de errores del backend con mensajes informativos

#### Componente de Gestión

**Archivo:** `src/components/SubtaskManager.tsx`

**Características:**
- Lista visual de todas las subtareas del usuario
- Botón "Nueva Subtarea" para abrir formulario de creación
- Edición inline (al hacer clic en botón Editar ✏️)
- Eliminación con validación (mínimo 1 subtarea)
- Estados de carga, error y éxito con mensajes informativos
- Diseño con cards que muestran: emoji, nombre, descripción y labels como badges

**Props:**
```typescript
interface SubtaskManagerProps {
  onSubtasksChange?: (subtasks: SubtaskDefinition[]) => void;
}
```

**Estados manejados:**
- `loading` - Carga inicial de subtareas
- `isCreating` - Muestra formulario de creación
- `editingId` - ID de subtarea en modo edición
- `message` / `messageType` - Feedback al usuario

**Estilos:** `src/components/SubtaskManager.css`
- Cards con hover effect
- Formularios inline con validación visual
- Badges para labels de Jira
- Responsive design para móviles

#### Integración en Settings

**Archivo:** `src/pages/SettingsPage.tsx`

```tsx
import { SubtaskManager } from '../components/SubtaskManager';

// ...

<div className="subtasks-config-section">
  <SubtaskManager />
</div>
```

**Ubicación:** Después de la sección de credenciales de Jira

#### Selector de Subtareas

**Archivo:** `src/components/SubtaskSelector.tsx`

**Cambios implementados:**
- Carga dinámica de subtareas desde backend al montar componente
- Auto-selección de todas las subtareas si ninguna está seleccionada
- Estado de loading mientras carga las subtareas
- IDs cambiados de string a number

```typescript
useEffect(() => {
  const loadSubtasks = async () => {
    try {
      const subtasks = await SubtaskService.getSubtasks();
      setAvailableSubtasks(subtasks);

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
```

#### Componente de Entrada de Tareas

**Archivo:** `src/components/MultiTaskInput.tsx`

**Cambios:**
- Campo `subtasks` en interface `Task` cambió de `string[]` a `number[]`
- Función `updateTask` actualizada para aceptar `number[]`:

```typescript
const updateTask = (
  id: string,
  field: 'text' | 'description' | 'assignee' | 'subtasks',
  value: string | string[] | number[] | undefined
) => {
  setTasks(tasks.map(t => t.id === id ? { ...t, [field]: value } : t));
};
```

## Flujo de Uso

### Usuario nuevo:
1. Usuario se registra en la aplicación
2. Al acceder por primera vez a "Configuración" → "Gestión de Subtareas"
3. El backend auto-inicializa 6 subtareas por defecto
4. Usuario puede editar, eliminar o agregar más subtareas
5. Al crear un workflow, el selector mostrará sus subtareas personalizadas

### Usuario existente:
1. Accede a Configuración (menú de usuario → Configuración)
2. Scroll down a la sección "Gestión de Subtareas"
3. Ve todas sus subtareas personalizadas en cards
4. Puede:
   - Crear nueva subtarea (botón "+ Nueva Subtarea")
   - Editar subtarea existente (botón ✏️)
   - Eliminar subtarea (botón 🗑️, con confirmación)
5. Los cambios se reflejan inmediatamente en el selector de subtareas

## Testing

**Script de prueba:** `test_subtasks_endpoint.sh`

Prueba completa del sistema:
1. Registro de usuario nuevo
2. Login y obtención de token JWT
3. GET subtareas (auto-inicialización)
4. POST crear subtarea personalizada
5. PUT actualizar subtarea
6. GET listar todas las subtareas
7. DELETE eliminar subtarea de prueba

**Ejecutar:**
```bash
./test_subtasks_endpoint.sh
```

## Verificación de Base de Datos

**Script:** `verify_db.py`

Verifica que:
- La tabla `subtask_templates` existe
- Todas las columnas están presentes
- La conexión a la base de datos funciona

**Ejecutar:**
```bash
source venv/bin/activate
python verify_db.py
```

## Estado Actual

### Backend: ✅ Completamente funcional
- Modelo de base de datos creado y migrado
- 5 endpoints CRUD + reorder implementados
- Auto-inicialización con defaults funcionando
- Validaciones implementadas (mínimo 1 subtarea)
- Autenticación JWT en todos los endpoints
- Filtrado por usuario funcionando

### Frontend: ✅ Completamente funcional
- SubtaskManager component con UI completa
- SubtaskService con todos los métodos CRUD
- Integración en SettingsPage
- SubtaskSelector actualizado para cargar dinámicamente
- MultiTaskInput soporta IDs numéricos
- Estilos responsive implementados

### Testing: ✅ Verificado
- Script de prueba del backend pasando exitosamente
- Auto-inicialización funcionando correctamente
- CRUD completo funcionando
- Validaciones funcionando (no eliminar última subtarea)

## Mejoras Futuras

1. **Drag & Drop para reordenar** - Implementar drag & drop en SubtaskManager
2. **Compartir templates** - Permitir compartir subtareas entre usuarios
3. **Templates predefinidos** - Ofrecer templates por industria (video, desarrollo, diseño)
4. **Colores personalizados** - Permitir asignar colores a las subtareas
5. **Categorías** - Agrupar subtareas por categorías (producción, post-producción, etc.)
6. **Export/Import** - Exportar e importar configuraciones de subtareas

## Archivos Modificados/Creados

### Backend
- ✅ `app/models/subtask.py` - Creado
- ✅ `app/models/__init__.py` - Modificado (añadido SubtaskTemplate)
- ✅ `app/api/routes/subtasks.py` - Creado
- ✅ `app/main.py` - Modificado (registro de router)

### Frontend
- ✅ `src/types/subtask.types.ts` - Modificado (IDs a number)
- ✅ `src/services/subtask.service.ts` - Creado
- ✅ `src/components/SubtaskManager.tsx` - Creado
- ✅ `src/components/SubtaskManager.css` - Creado
- ✅ `src/components/SubtaskSelector.tsx` - Modificado (carga dinámica)
- ✅ `src/components/MultiTaskInput.tsx` - Modificado (number[])
- ✅ `src/pages/SettingsPage.tsx` - Modificado (añadido SubtaskManager)
- ✅ `src/pages/Settings.css` - Modificado (estilos para sección)

### Testing y Utilidades
- ✅ `test_subtasks_endpoint.sh` - Creado
- ✅ `verify_db.py` - Creado
- ✅ `SUBTASKS_SYSTEM.md` - Creado (este documento)

## Servidores en Ejecución

- **Backend:** `http://localhost:8000` (uvicorn con --reload)
- **Frontend:** `http://localhost:3000` (react-scripts start)
- **Base de datos:** SQLite en `jira_agent.db`

## Conclusión

El sistema de gestión de subtareas personalizadas está completamente implementado y funcional. Los usuarios pueden crear, editar y eliminar sus propias plantillas de subtareas, y estas aparecen automáticamente en el selector al crear workflows. El sistema incluye auto-inicialización con valores por defecto sensatos para usuarios nuevos.
