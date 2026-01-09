"""
Instagram content creation endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.parsers.task_parser import create_parser
from app.clients.jira_client import JiraClient, JiraAPIError
from app.services.reel_workflow_service import ReelWorkflowService
from app.api.dependencies import get_jira_client, get_reel_workflow_service


router = APIRouter(tags=["Instagram Content"])


# ============================================================================
# Pydantic Models
# ============================================================================

class CreateInstagramContentRequest(BaseModel):
    """Request para crear contenido de Instagram."""

    text: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Texto en lenguaje natural describiendo el contenido",
        example="Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago",
        examples=[
            "Crear reel sobre viaje a Cartagena, alta prioridad",
            "Crear carrusel de tips de viaje",
            "Hacer historia sobre el hotel en Maldivas"
        ]
    )
    description: Optional[str] = Field(
        None,
        max_length=5000,
        description="Descripción detallada adicional del contenido (opcional)",
        example="Serie de 10 imágenes mostrando los mejores restaurantes con precios, menú estrella y tips para reservar."
    )
    project_key: str = Field(
        default="KAN",
        description="Clave del proyecto de Jira",
        example="KAN"
    )


class SubtaskInfo(BaseModel):
    """Información de una subtarea."""

    key: str = Field(..., description="Clave de la subtarea", example="KAN-124")
    phase: str = Field(..., description="Fase de producción", example="Idea / Concepto")
    emoji: str = Field(..., description="Emoji identificador", example="💡")
    url: str = Field(..., description="URL de la subtarea en Jira")


class CreateInstagramContentResponse(BaseModel):
    """Response al crear contenido de Instagram."""

    success: bool = Field(default=True)
    main_task_key: str = Field(..., description="Clave de la tarea principal", example="KAN-123")
    main_task_url: str = Field(..., description="URL de la tarea principal en Jira")
    content_type: str = Field(..., description="Tipo de contenido detectado", example="Reel", examples=["Reel", "Historia", "Carrusel"])
    subtasks: List[SubtaskInfo] = Field(..., description="Lista de subtareas creadas")
    total_tasks: int = Field(..., description="Total de tareas creadas (1 principal + subtareas)")


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/instagram", response_model=CreateInstagramContentResponse)
async def create_instagram_content(
    request: CreateInstagramContentRequest,
    service: ReelWorkflowService = Depends(get_reel_workflow_service),
    jira_client: JiraClient = Depends(get_jira_client)
):
    """
    Crea contenido de Instagram (Reel, Historia o Carrusel) con workflow completo.

    Proceso:
    1. Parsea el texto en lenguaje natural
    2. Detecta automáticamente: tipo de contenido, prioridad, assignee, labels
    3. Crea tarea principal + 6 subtareas de producción
    4. Retorna el key de la tarea principal y subtareas

    Args:
        request: Objeto con 'text' (descripción natural) y 'project_key' (opcional)

    Returns:
        CreateInstagramContentResponse con main_task_key y lista de subtasks

    Raises:
        HTTPException 400: Error de validación o parsing
        HTTPException 401: Error de autenticación con Jira
        HTTPException 500: Error interno del servidor
    """
    try:
        # 1. Parsear texto
        parser = create_parser(use_llm=False)
        parsed_task = parser.parse(request.text)

        # 2. Detectar tipo de contenido (Reel, Historia o Carrusel)
        content_type = "Reel"  # Default
        text_lower = request.text.lower()

        if "carrusel" in text_lower or "carousel" in text_lower:
            content_type = "Carrusel"
        elif "historia" in text_lower or "story" in text_lower or "stories" in text_lower:
            content_type = "Historia"

        # 3. Buscar Account ID si hay assignee
        assignee_account_id = None
        if parsed_task.assignee:
            assignee_account_id = jira_client.get_user_account_id(
                parsed_task.assignee,
                request.project_key
            )

        # 4. Crear workflow completo
        # Usar la descripción del request si existe, sino usar la del parsed_task
        final_description = request.description if request.description else parsed_task.description

        result = service.create_reel_workflow(
            project_key=request.project_key,
            title=parsed_task.summary,
            content_type=content_type,
            priority=parsed_task.priority,
            labels=parsed_task.labels,
            assignee=assignee_account_id,
            description=final_description
        )

        # 5. Formatear respuesta
        subtasks_info = [
            SubtaskInfo(
                key=subtask["key"],
                phase=subtask["phase"],
                emoji=subtask["emoji"],
                url=subtask["url"]
            )
            for subtask in result["subtasks"]
        ]

        return CreateInstagramContentResponse(
            success=True,
            main_task_key=result["main_task"]["key"],
            main_task_url=result["main_task"]["url"],
            content_type=content_type,
            subtasks=subtasks_info,
            total_tasks=result["total_tasks"]
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al parsear el texto: {str(e)}"
        )

    except JiraAPIError as e:
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
            detail=f"Error inesperado al crear contenido: {str(e)}"
        )
