"""
Batch Instagram content creation endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional

from app.parsers.task_parser import create_parser
from app.clients.jira_client import JiraClient, JiraAPIError
from app.services.reel_workflow_service import ReelWorkflowService
from app.api.dependencies import get_user_jira_client


router = APIRouter(tags=["Batch Tasks"])


# ============================================================================
# Pydantic Models
# ============================================================================

class TaskItem(BaseModel):
    """Modelo para una tarea individual en el batch."""

    text: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Texto en lenguaje natural describiendo el contenido de Instagram",
        example="Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago",
        examples=[
            "Crear reel sobre viaje a Cartagena, alta prioridad",
            "Crear carrusel de tips de viaje",
            "Historia de receta de arepas"
        ]
    )
    description: Optional[str] = Field(
        None,
        max_length=5000,
        description="Descripción detallada adicional del contenido (opcional)",
        example="Serie de 10 imágenes mostrando los mejores restaurantes con precios."
    )
    assignee: Optional[str] = Field(
        None,
        description="Account ID del usuario a asignar (opcional)",
        example="5b10ac8d82e05b22cc7d4ef5"
    )
    subtasks: Optional[List[str]] = Field(
        None,
        description="IDs de subtareas a crear (opcional). Valores posibles: seleccion, edicion, audio, color, copy, export",
        example=["seleccion", "edicion", "audio", "color", "copy", "export"]
    )


class CreateBatchTasksRequest(BaseModel):
    """Request para crear múltiples workflows de Instagram."""

    tasks: List[TaskItem] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Array de contenidos de Instagram a crear (máximo 50)",
        example=[
            {"text": "Crear reel sobre viaje a Cartagena, alta prioridad, asignado a santiago"},
            {"text": "Carrusel de tips de fotografía"},
            {"text": "Historia de receta de arepas, asignado a santiago"}
        ]
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


class TaskResult(BaseModel):
    """Resultado de crear un workflow de Instagram."""

    success: bool = Field(..., description="Si el workflow se creó exitosamente")
    main_task_key: Optional[str] = Field(None, description="Clave de la tarea principal", example="KAN-123")
    main_task_url: Optional[str] = Field(None, description="URL de la tarea principal en Jira")
    content_type: Optional[str] = Field(None, description="Tipo de contenido (Reel/Historia/Carrusel)", example="Reel", examples=["Reel", "Historia", "Carrusel"])
    subtasks: Optional[List[SubtaskInfo]] = Field(None, description="Lista de subtareas creadas")
    total_tasks: Optional[int] = Field(None, description="Total de tareas creadas (1 principal + subtareas)")
    error: Optional[str] = Field(None, description="Mensaje de error si falló")
    original_text: str = Field(..., description="Texto original de la tarea")


class CreateBatchTasksResponse(BaseModel):
    """Response al crear múltiples workflows de Instagram."""

    success: bool = Field(..., description="Si el batch se procesó completamente")
    total_requested: int = Field(..., description="Total de workflows solicitados")
    total_created: int = Field(..., description="Total de workflows creados exitosamente")
    total_failed: int = Field(..., description="Total de workflows que fallaron")
    total_tasks_created: int = Field(..., description="Total de tareas de Jira creadas (principales + subtareas)")
    results: List[TaskResult] = Field(..., description="Resultados individuales de cada workflow")


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/batch", response_model=CreateBatchTasksResponse)
async def create_batch_tasks(
    request: CreateBatchTasksRequest,
    jira_client: JiraClient = Depends(get_user_jira_client)
):
    """
    Crea múltiples workflows de Instagram (Reels/Historias/Carruseles) a partir de un array de textos.

    Requiere autenticación con JWT token.

    Cada tarea genera:
    - 1 tarea principal
    - 6 subtareas (fases de producción)
    - Total: 7 tareas de Jira por cada item del batch

    Proceso:
    1. Parsea cada texto en lenguaje natural
    2. Detecta tipo de contenido (Reel, Historia o Carrusel)
    3. Crea workflow completo con subtareas usando las credenciales del usuario
    4. Retorna un resumen con éxitos y fallos

    Args:
        request: Objeto con array de 'tasks' y 'project_key'
        jira_client: Cliente de Jira con credenciales del usuario (inyectado)

    Returns:
        CreateBatchTasksResponse con resultados de cada workflow

    Raises:
        HTTPException 400: Error de validación
        HTTPException 401: Error de autenticación con Jira
        HTTPException 500: Error interno del servidor

    Notes:
        - Se procesarán todos los workflows aunque algunos fallen
        - El endpoint retorna 200 incluso si algunos workflows fallan
        - Máximo 50 workflows por request (cada uno crea 7 tareas)
    """
    try:
        # Crear servicio de workflow con el JiraClient del usuario
        service = ReelWorkflowService(jira_client)

        parser = create_parser(use_llm=False)
        results = []
        total_created = 0
        total_failed = 0
        total_jira_tasks = 0

        for task_item in request.tasks:
            try:
                # 1. Parsear texto
                parsed_task = parser.parse(task_item.text)

                # 2. Detectar tipo de contenido (Reel, Historia o Carrusel)
                content_type = "Reel"  # Default
                text_lower = task_item.text.lower()

                if "carrusel" in text_lower or "carousel" in text_lower:
                    content_type = "Carrusel"
                elif "historia" in text_lower or "story" in text_lower or "stories" in text_lower:
                    content_type = "Historia"

                # 3. Determinar assignee (prioridad: task_item.assignee > parsed_task.assignee)
                assignee_account_id = None
                if task_item.assignee:
                    # Si viene del frontend (ya es un account_id), usarlo directamente
                    assignee_account_id = task_item.assignee
                elif parsed_task.assignee:
                    # Si viene del texto parseado (es un nombre), buscar el account_id
                    try:
                        assignee_account_id = jira_client.get_user_account_id(
                            parsed_task.assignee,
                            request.project_key
                        )
                    except Exception as e:
                        # Si falla buscar el usuario, continuar sin assignee
                        print(f"Warning: No se pudo encontrar usuario '{parsed_task.assignee}': {e}")

                # 4. Crear workflow completo
                # Usar la descripción del task_item si existe, sino usar la del parsed_task
                final_description = task_item.description if task_item.description else parsed_task.description

                workflow_result = service.create_reel_workflow(
                    project_key=request.project_key,
                    title=parsed_task.summary,
                    content_type=content_type,
                    priority=parsed_task.priority,
                    labels=parsed_task.labels,
                    assignee=assignee_account_id,
                    description=final_description,
                    subtask_ids=task_item.subtasks
                )

                # 5. Formatear subtareas
                subtasks_info = [
                    SubtaskInfo(
                        key=subtask["key"],
                        phase=subtask["phase"],
                        emoji=subtask["emoji"],
                        url=subtask["url"]
                    )
                    for subtask in workflow_result["subtasks"]
                ]

                # Éxito
                results.append(TaskResult(
                    success=True,
                    main_task_key=workflow_result["main_task"]["key"],
                    main_task_url=workflow_result["main_task"]["url"],
                    content_type=content_type,
                    subtasks=subtasks_info,
                    total_tasks=workflow_result["total_tasks"],
                    original_text=task_item.text
                ))
                total_created += 1
                total_jira_tasks += workflow_result["total_tasks"]

            except Exception as e:
                # Fallo en este workflow específico
                results.append(TaskResult(
                    success=False,
                    error=str(e),
                    original_text=task_item.text
                ))
                total_failed += 1

        return CreateBatchTasksResponse(
            success=total_failed == 0,
            total_requested=len(request.tasks),
            total_created=total_created,
            total_failed=total_failed,
            total_tasks_created=total_jira_tasks,
            results=results
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
            detail=f"Error inesperado al crear workflows: {str(e)}"
        )
