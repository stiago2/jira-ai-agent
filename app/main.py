"""
FastAPI application entry point.

Implementa endpoints para crear issues de Jira desde texto en lenguaje natural.
"""

from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from app.parsers.task_parser import create_parser, ParsedTask
from app.clients.jira_client import JiraAPIError, JiraClient
from app.api.routes import instagram, batch_tasks, projects, auth, subtasks
from app.api.dependencies import get_jira_client, get_user_jira_client, get_current_user
from app.models.user import User
from app.core.config import settings


# ============================================================================
# Pydantic Models
# ============================================================================

class CreateTaskRequest(BaseModel):
    """Request para crear tarea desde texto natural."""

    text: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Texto en lenguaje natural describiendo la tarea",
        example="Crea una tarea para editar el reel de Komodo, prioridad alta, asignada a Juan"
    )
    project_key: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Clave del proyecto de Jira (ej: PROJ, DEV, etc.)",
        example="PROJ"
    )


class CreateTaskResponse(BaseModel):
    """Respuesta al crear una tarea."""

    success: bool = Field(..., description="Indica si la operación fue exitosa")
    issue_key: str = Field(..., description="Clave del issue creado (ej: PROJ-123)", example="PROJ-123")
    issue_url: str = Field(..., description="URL del issue en Jira")
    parsed_data: dict = Field(..., description="Datos parseados del texto")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Nivel de confianza del parsing (0-1)")


class ParsePreviewResponse(BaseModel):
    """Respuesta para preview del parsing sin crear el issue."""

    summary: str
    description: str
    issue_type: str
    priority: str
    assignee: Optional[str] = None
    labels: List[str] = []
    confidence: float = Field(..., ge=0.0, le=1.0)


class ErrorResponse(BaseModel):
    """Respuesta de error."""

    success: bool = False
    error: str
    detail: Optional[str] = None


class JiraProject(BaseModel):
    """Información de un proyecto de Jira."""

    key: str = Field(..., description="Clave del proyecto (ej: KAN, PROJ)", example="KAN")
    name: str = Field(..., description="Nombre del proyecto", example="Instagram Reels")
    project_type: str = Field(..., description="Tipo de proyecto", example="software")


class ProjectsListResponse(BaseModel):
    """Respuesta al listar proyectos."""

    success: bool = True
    total: int = Field(..., description="Total de proyectos encontrados")
    projects: List[JiraProject] = Field(..., description="Lista de proyectos disponibles")


# ============================================================================
# FastAPI App
# ============================================================================

app = FastAPI(
    title="Jira AI Agent",
    description="AI Agent that creates Jira tasks from natural language",
    version="0.2.0",
)

# Configure CORS
# Usar CORS_ORIGINS de settings (variable de entorno)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(subtasks.router, prefix="/api/v1")
app.include_router(instagram.router, prefix="/api/v1/content")
app.include_router(batch_tasks.router, prefix="/api/v1/tasks")
app.include_router(projects.router, prefix="/api/v1")


# ============================================================================
# Dependency Injection / Singletons
# ============================================================================

def get_parser():
    """Obtiene instancia del parser."""
    # Por ahora usa el parser basado en reglas
    # En el futuro se puede cambiar a LLM con: create_parser(use_llm=True, ...)
    return create_parser(use_llm=False)


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Jira AI Agent",
        "version": "0.2.0",
        "status": "running",
        "authentication": "enabled",
        "endpoints": {
            "health": "/api/v1/health",
            "auth": {
                "register": "/api/v1/auth/register",
                "login": "/api/v1/auth/login",
                "me": "/api/v1/auth/me",
                "logout": "/api/v1/auth/logout"
            },
            "projects": "/api/v1/projects",
            "project_users": "/api/v1/projects/{project_key}/users",
            "create_task": "/api/v1/tasks/create",
            "parse_preview": "/api/v1/tasks/parse",
            "create_batch_tasks": "/api/v1/tasks/batch",
            "create_instagram_content": "/api/v1/content/instagram"
        },
        "docs": "/docs"
    }


@app.get("/api/v1/health")
async def health_check():
    """
    Health check endpoint.

    Verifica que la API está funcionando.
    """
    try:
        # Verificar si hay credenciales de Jira configuradas globalmente
        jira_configured = bool(settings.JIRA_BASE_URL and settings.JIRA_EMAIL and settings.JIRA_API_TOKEN)

        response = {
            "status": "healthy",
            "parser": "rule-based",
            "database": "connected" if settings.DATABASE_URL else "not configured"
        }

        if jira_configured:
            try:
                jira_client = get_jira_client()
                user = jira_client.get_current_user()
                response["jira_connection"] = "ok"
                response["jira_user"] = user.get("displayName", "unknown")
            except Exception as e:
                response["jira_connection"] = "error"
                response["jira_error"] = str(e)
        else:
            response["jira_connection"] = "not configured (per-user credentials)"

        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error al verificar salud del servicio: {str(e)}"
        )


@app.get("/api/v1/projects", response_model=ProjectsListResponse)
async def list_projects(
    jira_client: JiraClient = Depends(get_user_jira_client)
):
    """
    Lista todos los proyectos disponibles en Jira del usuario autenticado.

    Requiere autenticación con JWT token.

    Args:
        jira_client: Cliente de Jira con credenciales del usuario (inyectado)

    Returns:
        ProjectsListResponse con la lista de proyectos disponibles

    Raises:
        HTTPException 401: Token inválido o expirado
        HTTPException 400: Usuario sin credenciales de Jira configuradas
        HTTPException 500: Error interno del servidor
    """
    try:

        # Obtener proyectos
        projects_data = jira_client._make_request("GET", "/project")

        # Formatear respuesta
        projects = []
        for project in projects_data:
            projects.append(
                JiraProject(
                    key=project.get("key", ""),
                    name=project.get("name", ""),
                    project_type=project.get("projectTypeKey", "unknown")
                )
            )

        return ProjectsListResponse(
            success=True,
            total=len(projects),
            projects=projects
        )

    except JiraAPIError as e:
        # Error específico de Jira API
        if e.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Error de autenticación con Jira: {str(e)}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de Jira API: {str(e)}"
            )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proyectos: {str(e)}"
        )


@app.post("/api/v1/tasks/parse", response_model=ParsePreviewResponse)
async def parse_task_preview(request: CreateTaskRequest):
    """
    Preview del parsing sin crear el issue.

    Útil para verificar cómo se interpretará el texto antes de crear el issue.
    """
    try:
        # Parsear texto
        parser = get_parser()
        result = parser.parse(request.text)

        return ParsePreviewResponse(
            summary=result.summary,
            description=result.description,
            issue_type=result.issue_type,
            priority=result.priority,
            assignee=result.assignee,
            labels=result.labels,
            confidence=result.confidence
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear el texto: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado: {str(e)}"
        )


@app.post("/api/v1/tasks/create", response_model=CreateTaskResponse)
async def create_task_from_text(
    request: CreateTaskRequest,
    jira_client: JiraClient = Depends(get_user_jira_client)
):
    """
    Crea un issue de Jira desde texto en lenguaje natural.

    Requiere autenticación con JWT token.

    Proceso:
    1. Parsea el texto usando el TaskParser
    2. Crea el issue en Jira usando las credenciales del usuario autenticado
    3. Retorna el issue key y URL

    Args:
        request: Objeto con 'text' (descripción natural) y 'project_key' (proyecto Jira)
        jira_client: Cliente de Jira con credenciales del usuario (inyectado)

    Returns:
        CreateTaskResponse con el issue_key, issue_url y datos parseados

    Raises:
        HTTPException 400: Error de validación o parsing
        HTTPException 401: Token inválido o expirado
        HTTPException 404: Proyecto no encontrado
        HTTPException 500: Error interno del servidor
    """
    try:
        # 1. Parsear el texto
        parser = get_parser()
        parsed_task = parser.parse(request.text)

        # 3. Si hay assignee, buscar el Account ID
        assignee_account_id = None
        if parsed_task.assignee:
            assignee_account_id = jira_client.get_user_account_id(
                parsed_task.assignee,
                request.project_key
            )
            if not assignee_account_id:
                print(f"⚠️  Usuario '{parsed_task.assignee}' no encontrado en Jira. El issue se creará sin asignar.")

        # 4. Crear issue en Jira
        jira_response = jira_client.create_issue(
            project_key=request.project_key,
            summary=parsed_task.summary,
            description=parsed_task.description,
            issue_type=parsed_task.issue_type,
            priority=parsed_task.priority,
            labels=parsed_task.labels,
            assignee=assignee_account_id  # Usar Account ID, no nombre
        )

        # 5. Construir respuesta
        issue_key = jira_response["key"]
        issue_url = f"{jira_client.base_url}/browse/{issue_key}"

        return CreateTaskResponse(
            success=True,
            issue_key=issue_key,
            issue_url=issue_url,
            parsed_data=parsed_task.to_dict(),
            confidence=parsed_task.confidence
        )

    except ValueError as e:
        # Error de validación o parsing
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear el texto: {str(e)}"
        )

    except JiraAPIError as e:
        # Error específico de Jira API
        if e.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Error de autenticación con Jira: {str(e)}"
            )
        elif e.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proyecto '{request.project_key}' no encontrado en Jira: {str(e)}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error de Jira API: {str(e)}"
            )

    except HTTPException:
        # Re-raise HTTPExceptions
        raise

    except Exception as e:
        # Error inesperado
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error inesperado al crear la tarea: {str(e)}"
        )


# ============================================================================
# Exception Handlers
# ============================================================================

@app.exception_handler(JiraAPIError)
async def jira_api_error_handler(request, exc: JiraAPIError):
    """Handler global para errores de Jira API."""
    return {
        "success": False,
        "error": "jira_api_error",
        "detail": str(exc),
        "status_code": exc.status_code
    }


@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Handler global para errores de validación."""
    return {
        "success": False,
        "error": "validation_error",
        "detail": str(exc)
    }


# ============================================================================
# Startup Event
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Evento ejecutado al iniciar la aplicación."""
    print("=" * 70)
    print("  JIRA AI AGENT - Starting...")
    print("=" * 70)

    print(f"✓ CORS Origins: {settings.CORS_ORIGINS}")
    print(f"✓ Database: {settings.DATABASE_URL[:50]}..." if len(settings.DATABASE_URL) > 50 else f"✓ Database: {settings.DATABASE_URL}")
    print(f"✓ JWT Algorithm: {settings.JWT_ALGORITHM}")

    print("\n✓ Servidor iniciado")
    print("  - Health check: http://localhost:8000/api/v1/health")
    print("  - Docs: http://localhost:8000/docs")
    print("=" * 70)
