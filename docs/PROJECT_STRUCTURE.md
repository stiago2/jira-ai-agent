# Estructura del Proyecto

## Árbol de Directorios

```
jira-ai-agent/
├── app/                          # Código fuente de la aplicación
│   ├── __init__.py
│   ├── main.py                   # Entry point FastAPI
│   │
│   ├── api/                      # API Layer
│   │   ├── __init__.py
│   │   ├── dependencies.py       # Dependency injection
│   │   └── routes/               # Endpoints
│   │       ├── __init__.py
│   │       ├── health.py         # Health checks
│   │       └── tasks.py          # Task endpoints
│   │
│   ├── core/                     # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py             # Settings & configuration
│   │   ├── exceptions.py         # Custom exceptions
│   │   └── logging.py            # Logging setup
│   │
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   ├── jira.py               # Jira domain models
│   │   ├── requests.py           # API request models
│   │   └── responses.py          # API response models
│   │
│   ├── services/                 # Business logic
│   │   ├── __init__.py
│   │   ├── ai_service.py         # AI/LLM processing
│   │   ├── jira_service.py       # Jira API client
│   │   └── task_orchestrator.py  # Main orchestrator
│   │
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── formatters.py         # Data formatters
│       └── validators.py         # Data validators
│
├── tests/                        # Tests
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   ├── unit/                     # Unit tests
│   │   └── __init__.py
│   └── integration/              # Integration tests
│       └── __init__.py
│
├── config/                       # Configuration files
│
├── docs/                         # Documentation
│   └── PROJECT_STRUCTURE.md      # This file
│
├── scripts/                      # Utility scripts
│   ├── run_dev.sh                # Development server
│   └── setup.sh                  # Setup script
│
├── .env.example                  # Environment variables example
├── .gitignore                    # Git ignore rules
├── docker-compose.yml            # Docker Compose config
├── Dockerfile                    # Docker image definition
├── pyproject.toml                # Python project config
├── README.md                     # Main documentation
├── requirements.txt              # Production dependencies
└── requirements-dev.txt          # Development dependencies
```

## Descripción de Módulos

### `/app/main.py`
Entry point de la aplicación FastAPI. Configura:
- CORS middleware
- Exception handlers
- Routers de la API

### `/app/api/routes/`
Define los endpoints HTTP:
- `health.py`: Health checks y status
- `tasks.py`: CRUD de tareas

### `/app/core/`
Funcionalidad core compartida:
- `config.py`: Configuración con Pydantic Settings
- `exceptions.py`: Excepciones personalizadas
- `logging.py`: Setup de logging

### `/app/models/`
Modelos de datos con Pydantic:
- `jira.py`: Modelos de dominio Jira (Issue, Project, etc.)
- `requests.py`: Schemas de requests HTTP
- `responses.py`: Schemas de responses HTTP

### `/app/services/`
Lógica de negocio:
- `ai_service.py`: Procesamiento con LLM
- `jira_service.py`: Cliente Jira REST API
- `task_orchestrator.py`: Orquesta el flujo completo

### `/app/utils/`
Utilidades helpers:
- `validators.py`: Validación de datos
- `formatters.py`: Formateo de datos

## Flujo de Datos

```
HTTP Request
    ↓
FastAPI Router (app/api/routes/)
    ↓
Task Orchestrator (app/services/task_orchestrator.py)
    ↓
    ├── AI Service (app/services/ai_service.py)
    └── Jira Service (app/services/jira_service.py)
    ↓
HTTP Response
```

## Archivos de Configuración

### `.env`
Variables de entorno (no versionado):
- Credenciales Jira
- API keys
- Configuración de servicios

### `requirements.txt`
Dependencias de producción

### `requirements-dev.txt`
Dependencias de desarrollo (testing, linting)

### `pyproject.toml`
Configuración del proyecto Python:
- Metadata del proyecto
- Herramientas (black, mypy, pytest)

### `docker-compose.yml`
Orquestación de servicios Docker:
- API service
- Redis (cache)

## Convenciones

### Naming
- **Files**: snake_case (e.g., `jira_service.py`)
- **Classes**: PascalCase (e.g., `JiraService`)
- **Functions**: snake_case (e.g., `create_task`)
- **Constants**: UPPER_CASE (e.g., `API_V1_PREFIX`)

### Imports
Ordenados por:
1. Standard library
2. Third-party packages
3. Local imports

### Docstrings
Formato Google style:
```python
def function(arg1: str, arg2: int) -> bool:
    """
    Brief description.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value
    """
```

## Testing

### Unit Tests
Ubicación: `tests/unit/`
- Testean funciones individuales
- Usan mocks para dependencias

### Integration Tests
Ubicación: `tests/integration/`
- Testean flujos completos
- Usan servicios reales (Jira test instance)

## Estado Actual

### ✅ Implementado
- Estructura completa del proyecto
- Modelos Pydantic
- Configuración base
- Esqueleto de servicios

### ⏳ Por Implementar
- Lógica de servicios completa
- Tests
- Documentación API detallada
- CI/CD pipeline
