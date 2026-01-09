# Jira Tracker - Frontend

Interfaz web para el Jira AI Agent. Permite crear tareas en Jira usando lenguaje natural.

## Características

- **Selector de proyectos**: Elige el proyecto de Jira en el que quieres trabajar
- **Creación de tareas con lenguaje natural**: Describe tu tarea y el sistema la parsea automáticamente
- **Workflow de Instagram**: Para el proyecto KAN, crea automáticamente workflows completos con 7 subtareas
- **Detección automática**: El parser detecta prioridad, assignee, etiquetas y más
- **Interfaz amigable**: UI moderna inspirada en los diseños de Atlassian

## Requisitos Previos

- Node.js 14 o superior
- npm o yarn
- Backend de Jira AI Agent corriendo en `http://localhost:8000`

## Instalación

1. Navega al directorio del proyecto:

```bash
cd jira-tracker
```

2. Instala las dependencias:

```bash
npm install
```

3. (Opcional) Configura la URL del backend:

```bash
cp .env.example .env
# Edita .env si tu backend está en una URL diferente
```

## Ejecutar en Desarrollo

```bash
npm start
```

La aplicación se abrirá en [http://localhost:3000](http://localhost:3000)

## Construir para Producción

```bash
npm run build
```

Los archivos optimizados estarán en la carpeta `build/`

## Estructura del Proyecto

```
jira-tracker/
├── public/              # Archivos estáticos
├── src/
│   ├── components/      # Componentes React reutilizables
│   │   ├── ErrorMessage.tsx
│   │   ├── LoadingSpinner.tsx
│   │   ├── ProjectSelector.tsx
│   │   ├── SuccessMessage.tsx
│   │   └── TaskInput.tsx
│   ├── pages/          # Páginas principales
│   │   ├── HomePage.tsx
│   │   └── ProjectWorkspace.tsx
│   ├── services/       # Servicios de API
│   │   └── api.service.ts
│   ├── types/          # TypeScript interfaces
│   │   └── api.types.ts
│   ├── App.tsx         # Componente principal
│   └── index.tsx       # Punto de entrada
└── package.json
```

## Uso

### 1. Página Principal

Al abrir la aplicación verás:
- Un dropdown con los proyectos de Jira disponibles
- Selecciona un proyecto para continuar

### 2. Workspace del Proyecto

Una vez seleccionado un proyecto:

#### Proyectos normales (tareas individuales):
- Escribe tu tarea en lenguaje natural
- Ejemplo: `"Corregir bug en login, prioridad alta, asignado a juan"`
- Click en "Crear Tarea"

#### Proyecto KAN (workflow de Instagram):
- Escribe la descripción del contenido
- Ejemplo: `"Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago"`
- El sistema detecta automáticamente si es Reel o Historia
- Se crean 7 subtareas automáticamente:
  1. Idea / Concepto 💡
  2. Grabación 🎬
  3. Edición ✂️
  4. Revisión 👀
  5. Aprobación ✅
  6. Publicación 📱
  7. Análisis 📊

### 3. Sintaxis del Parser

El parser detecta automáticamente:

- **Prioridad**: "alta prioridad", "prioridad baja", "urgente", etc.
- **Assignee**: "asignado a santiago", "asignar a juan"
- **Etiquetas**: "etiquetas: backend, api", "tags: bug, hotfix"
- **Tipo de contenido** (KAN): "reel", "historia", "story"

Ejemplos:

```
"Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago"
→ Summary: "Sobre viaje a cartagena"
→ Priority: High
→ Assignee: santiago
→ Type: Reel
```

```
"Corregir error en API de pagos, crítica, etiquetas: backend, hotfix"
→ Summary: "Corregir error en api de pagos"
→ Priority: Highest
→ Labels: ["backend", "hotfix"]
```

## Endpoints Utilizados

La aplicación se conecta a estos endpoints del backend:

- `GET /api/v1/projects` - Lista proyectos disponibles
- `POST /api/v1/tasks/create` - Crea tarea individual
- `POST /api/v1/content/instagram` - Crea workflow de Instagram

## Configuración del Backend

Asegúrate de que el backend esté corriendo antes de usar esta aplicación:

```bash
# En el directorio raíz del proyecto
cd ..
uvicorn app.main:app --reload
```

## Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `REACT_APP_API_URL` | URL del backend API | `http://localhost:8000` |

## Scripts Disponibles

- `npm start` - Ejecuta en modo desarrollo
- `npm run build` - Construye para producción
- `npm test` - Ejecuta tests
- `npm run eject` - Expone configuración de webpack (irreversible)

## Tecnologías Utilizadas

- **React 18** - Framework UI
- **TypeScript** - Type safety
- **React Router v6** - Routing
- **CSS Modules** - Estilos scoped

## Soporte de Navegadores

- Chrome (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)
- Edge (últimas 2 versiones)

## Troubleshooting

### Error: "Error al cargar los proyectos"

- Verifica que el backend esté corriendo
- Verifica que la URL en `.env` sea correcta
- Verifica que las credenciales de Jira estén configuradas en el backend

### Error: "Error al crear la tarea"

- Verifica que el proyecto exista en Jira
- Verifica que el assignee tenga acceso al proyecto
- Revisa los logs del backend para más detalles

## Licencia

MIT

## Autor

Santiago Florez Giraldo
