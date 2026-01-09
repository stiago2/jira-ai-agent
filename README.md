# Jira AI Agent

🤖 Agente de IA que **crea tareas de Jira desde texto en lenguaje natural** usando FastAPI y Python.

Simplemente escribe qué necesitas hacer y el agente lo convierte automáticamente en un issue de Jira con el tipo, prioridad y campos apropiados.

## ✨ ¿Qué hace este proyecto?

Convierte texto como este:

```
"Crear tarea urgente para editar el reel de Komodo, prioridad alta, asignada a Juan"
```

En un issue de Jira estructurado:
- **Summary**: "Editar el reel de komodo"
- **Issue Type**: Task
- **Priority**: High
- **Assignee**: Juan
- **Labels**: [video]

## 🚀 Características

- ✅ **API REST** con FastAPI
- ✅ **Integración completa con Jira Cloud** (REST API v3)
- ✅ **Parser basado en reglas** para procesamiento de lenguaje natural
- ✅ **Preparado para LLM** (OpenAI, Anthropic, etc.)
- ✅ **Validación robusta** con Pydantic
- ✅ **Documentación interactiva** (Swagger/ReDoc)
- ✅ **Docker ready**

## 📋 Requisitos

- Python 3.11+
- Cuenta de Jira Cloud
- API Token de Jira

## 🛠️ Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd jira-ai-agent
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de Jira:

```env
JIRA_BASE_URL=https://tu-empresa.atlassian.net
JIRA_EMAIL=tu-email@empresa.com
JIRA_API_TOKEN=tu_api_token_aqui
JIRA_DEFAULT_PROJECT=PROJ
```

## 🔑 Cómo obtener tu API Token de Jira

1. Ve a: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click en **"Create API token"**
3. Dale un nombre (ej: "jira-ai-agent")
4. Copia el token generado
5. Pégalo en `.env` como `JIRA_API_TOKEN`

**Importante**: El token es como una contraseña. Nunca lo compartas ni lo comitees a git.

## ▶️ Ejecutar el servidor

### Modo desarrollo (con auto-reload)

```bash
uvicorn app.main:app --reload
```

### Modo producción

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

## 📚 Documentación Interactiva

Una vez el servidor esté corriendo:

- **Swagger UI** (interfaz interactiva): http://localhost:8000/docs
- **ReDoc** (documentación): http://localhost:8000/redoc

## 🎯 Uso - Ejemplo con cURL

### 1. Verificar que el servidor funciona

```bash
curl http://localhost:8000/api/v1/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "jira_connection": "ok",
  "jira_user": "Tu Nombre",
  "parser": "rule-based"
}
```

### 2. Preview del parsing (sin crear el issue)

```bash
curl -X POST http://localhost:8000/api/v1/tasks/parse \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bug crítico en el login de mobile, asignar a Pedro",
    "project_key": "PROJ"
  }'
```

**Respuesta:**
```json
{
  "summary": "Bug crítico en el login de mobile",
  "description": "Bug crítico en el login de mobile, asignar a Pedro",
  "issue_type": "Bug",
  "priority": "Highest",
  "assignee": "Pedro",
  "labels": ["mobile", "urgent"],
  "confidence": 0.85
}
```

### 3. Crear issue en Jira desde texto natural

```bash
curl -X POST http://localhost:8000/api/v1/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Implementar autenticación OAuth2 para el backend API, prioridad alta",
    "project_key": "PROJ"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "issue_key": "PROJ-123",
  "issue_url": "https://tu-empresa.atlassian.net/browse/PROJ-123",
  "parsed_data": {
    "summary": "Implementar autenticación oauth2 para el backend api",
    "description": "Implementar autenticación OAuth2 para el backend API, prioridad alta",
    "issue_type": "Task",
    "priority": "High",
    "assignee": null,
    "labels": ["backend", "security"],
    "confidence": 0.85
  },
  "confidence": 0.85
}
```

### 4. Más ejemplos de texto que el parser entiende

```bash
# User Story
"Como usuario quiero exportar datos a CSV para analizarlos offline"

# Bug con prioridad
"Arreglar error crítico en el sistema de pagos ASAP"

# Tarea con asignado
"Documentar la API REST para María, baja prioridad"

# Epic
"Epic para implementar el módulo de reportes completo"
```

## 📊 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Información básica de la API |
| GET | `/api/v1/health` | Health check y verificación de conexión |
| POST | `/api/v1/tasks/parse` | Preview del parsing sin crear issue |
| POST | `/api/v1/tasks/create` | Crear issue en Jira desde texto |

## 🔍 Palabras Clave Soportadas

### Tipos de Issue
- **Bug**: bug, error, falla, arreglar, fix
- **Story**: historia, story, como usuario
- **Epic**: epic, épica, iniciativa
- **Task**: tarea, task, crear, implementar, desarrollar

### Prioridades
- **Highest**: crítico, urgente, ASAP, bloqueante
- **High**: alta, importante, prioritario
- **Medium**: media, normal (default)
- **Low**: baja, menor
- **Lowest**: muy baja, trivial

### Asignación
- "asignada a Juan"
- "para María"
- "que lo haga Pedro"
- "@Ana"

Ver documentación completa en: [app/parsers/README.md](app/parsers/README.md)

## 🐳 Docker

```bash
# Construir y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Detener
docker-compose down
```

## 🧪 Tests

```bash
# Ejecutar tests del parser
pytest tests/unit/test_task_parser.py -v

# Ejecutar ejemplo del parser
python3 examples/test_task_parser.py

# Ejecutar ejemplo del cliente de Jira
python3 examples/test_jira_client.py
```

## 📁 Estructura del Proyecto

```
jira-ai-agent/
├── app/
│   ├── main.py              # FastAPI app principal
│   ├── clients/
│   │   ├── jira_client.py   # Cliente de Jira API
│   │   └── README.md        # Documentación del cliente
│   ├── parsers/
│   │   ├── task_parser.py   # Parser de texto natural
│   │   └── README.md        # Documentación del parser
│   ├── api/                 # Endpoints FastAPI
│   ├── core/                # Configuración y excepciones
│   ├── models/              # Modelos Pydantic
│   └── services/            # Lógica de negocio
├── tests/
│   └── unit/                # Tests unitarios
├── examples/                # Scripts de ejemplo
├── requirements.txt         # Dependencias Python
├── .env.example            # Template de variables de entorno
├── Dockerfile              # Configuración Docker
└── docker-compose.yml      # Orquestación Docker
```

## 🎓 Componentes Principales

### 1. **TaskParser** ([app/parsers/task_parser.py](app/parsers/task_parser.py))
Parser basado en reglas que extrae información estructurada del texto natural.

- Detección de tipo de issue (Task, Bug, Story, Epic)
- Extracción de prioridad (Highest a Lowest)
- Identificación de asignado
- Generación automática de labels
- Score de confianza (0.0-1.0)

### 2. **JiraClient** ([app/clients/jira_client.py](app/clients/jira_client.py))
Cliente completo para Jira REST API v3.

- Autenticación con Basic Auth (email + API token)
- Creación de issues con ADF (Atlassian Document Format)
- Manejo robusto de errores
- Métodos: create_issue, get_issue, get_project, test_connection

### 3. **FastAPI Endpoints** ([app/main.py](app/main.py))
API REST que conecta el parser con Jira.

- Validación con Pydantic
- Manejo de errores HTTP
- CORS configurado
- Exception handlers globales

## 🔮 Estado del Proyecto

### ✅ Implementado
- ✅ Cliente completo de Jira API
- ✅ Parser basado en reglas con alta precisión
- ✅ Endpoints FastAPI funcionando
- ✅ Validación con Pydantic
- ✅ Documentación completa
- ✅ Tests unitarios del parser
- ✅ Ejemplos de uso
- ✅ Docker support

### 🚧 Próximas Mejoras
- 🔄 Integración con LLM (OpenAI/Anthropic) para parsing avanzado
- 🔄 Cache con Redis para reducir llamadas a Jira
- 🔄 Rate limiting
- 🔄 Tests de integración end-to-end
- 🔄 Webhook callbacks
- 🔄 Integración con Slack

## 🤖 Migración a LLM (Futuro)

El código está preparado para usar un LLM en lugar del parser basado en reglas:

```python
# Actualmente (rule-based)
parser = create_parser(use_llm=False)

# En el futuro (LLM-based)
parser = create_parser(
    use_llm=True,
    api_key="sk-...",
    model="gpt-4"
)
```

Ver [app/parsers/README.md](app/parsers/README.md) para más detalles.

## 🐛 Troubleshooting

### Error: "Error de configuración de Jira"
- Verifica que `.env` existe y tiene las variables correctas
- Asegúrate de que `JIRA_BASE_URL` no tenga `/` al final
- Verifica que el API token es válido

### Error 401: "Error de autenticación"
- El API token puede haber expirado
- Verifica que el email es correcto
- Genera un nuevo API token en Jira

### Error 404: "Proyecto no encontrado"
- Verifica que el `project_key` existe en tu Jira
- Asegúrate de tener permisos en el proyecto

## 📄 Licencia

MIT License

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -m 'Agregar nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

## 📞 Soporte

Para reportar bugs o sugerir mejoras, abre un issue en el repositorio.
