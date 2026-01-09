"""
Task management endpoints.
"""

from fastapi import APIRouter, HTTPException, status

from app.models.requests import CreateTaskRequest, PreviewTaskRequest
from app.models.responses import (
    TaskCreatedResponse,
    TaskPreviewResponse,
    MetadataResponse,
    ErrorResponse
)
from app.core.logging import logger

router = APIRouter()


@router.post(
    "/tasks/create",
    response_model=TaskCreatedResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def create_task(request: CreateTaskRequest):
    """
    Create a Jira task from natural language text.

    Args:
        request: CreateTaskRequest with text and project key

    Returns:
        TaskCreatedResponse with created issue details
    """
    logger.info(f"Creating task for project {request.project_key}")

    # TODO: Implement task creation logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Task creation not yet implemented"
    )


@router.post(
    "/tasks/preview",
    response_model=TaskPreviewResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def preview_task(request: PreviewTaskRequest):
    """
    Preview how a task will be created without actually creating it.

    Args:
        request: PreviewTaskRequest with text and project key

    Returns:
        TaskPreviewResponse with extracted task details
    """
    logger.info(f"Previewing task for project {request.project_key}")

    # TODO: Implement preview logic
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Task preview not yet implemented"
    )


@router.get(
    "/tasks/metadata",
    response_model=MetadataResponse,
    responses={
        500: {"model": ErrorResponse}
    }
)
async def get_metadata(project_key: str = None):
    """
    Get Jira metadata (projects, issue types, priorities).

    Args:
        project_key: Optional project key to filter metadata

    Returns:
        MetadataResponse with available Jira metadata
    """
    logger.info(f"Getting metadata for project {project_key}")

    # TODO: Implement metadata retrieval
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Metadata retrieval not yet implemented"
    )
