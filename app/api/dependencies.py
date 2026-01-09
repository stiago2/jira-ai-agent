"""
API dependencies for dependency injection.
"""

from fastapi import HTTPException, status

from app.core.config import settings
from app.services.jira_service import JiraService
from app.services.ai_service import AIService
from app.services.task_orchestrator import TaskOrchestrator
from app.clients.jira_client import JiraClient
from app.services.reel_workflow_service import ReelWorkflowService


def get_jira_service() -> JiraService:
    """
    Get Jira service instance.

    Returns:
        JiraService instance
    """
    return JiraService(
        base_url=settings.JIRA_BASE_URL,
        email=settings.JIRA_EMAIL,
        api_token=settings.JIRA_API_TOKEN
    )


def get_ai_service() -> AIService:
    """
    Get AI service instance.

    Returns:
        AIService instance
    """
    return AIService()


def get_task_orchestrator() -> TaskOrchestrator:
    """
    Get task orchestrator instance.

    Returns:
        TaskOrchestrator instance
    """
    return TaskOrchestrator(
        jira_service=get_jira_service(),
        ai_service=get_ai_service()
    )


def get_jira_client() -> JiraClient:
    """
    Get JiraClient instance with configuration from environment variables.

    Returns:
        JiraClient: Configured Jira client instance

    Raises:
        HTTPException: If configuration is invalid or missing
    """
    try:
        return JiraClient()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error de configuración de Jira: {str(e)}"
        )


def get_reel_workflow_service() -> ReelWorkflowService:
    """
    Get ReelWorkflowService instance with JiraClient dependency.

    Returns:
        ReelWorkflowService: Configured workflow service instance

    Raises:
        HTTPException: If JiraClient initialization fails
    """
    jira_client = get_jira_client()
    return ReelWorkflowService(jira_client)
