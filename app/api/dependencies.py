"""
API dependencies for dependency injection.
"""

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User
from app.services.jira_service import JiraService
from app.services.ai_service import AIService
from app.services.task_orchestrator import TaskOrchestrator
from app.clients.jira_client import JiraClient
from app.services.reel_workflow_service import ReelWorkflowService

# Security scheme for JWT
security = HTTPBearer()


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


# ============================================================================
# Authentication Dependencies
# ============================================================================

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT token.

    This dependency should be used in endpoints that require authentication.

    Args:
        credentials: HTTP Bearer token from Authorization header
        db: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException 401: If token is invalid or expired
        HTTPException 403: If user is inactive

    Example:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}
    """
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: falta subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current user and verify they are a superuser.

    Args:
        current_user: The authenticated user

    Returns:
        User: The authenticated superuser

    Raises:
        HTTPException 403: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user


def get_user_jira_client(current_user: User = Depends(get_current_user)) -> JiraClient:
    """
    Get JiraClient instance with the current user's Jira credentials.

    This dependency should be used in endpoints that need to interact with Jira
    on behalf of the authenticated user.

    Args:
        current_user: The authenticated user (injected by dependency)

    Returns:
        JiraClient: Configured with user's Jira credentials

    Raises:
        HTTPException 400: If user hasn't configured Jira credentials
        HTTPException 500: If JiraClient initialization fails

    Example:
        @app.get("/projects")
        def list_projects(jira_client: JiraClient = Depends(get_user_jira_client)):
            return jira_client.get_projects()
    """
    from app.core.encryption import decrypt_token

    # Validate user has Jira credentials configured
    if not current_user.jira_base_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no tiene configurada la URL de Jira. Por favor, actualiza tu perfil."
        )

    if not current_user.jira_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no tiene configurado el email de Jira. Por favor, actualiza tu perfil."
        )

    if not current_user.jira_api_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no tiene configurado el token de Jira. Por favor, actualiza tu perfil."
        )

    try:
        # Decrypt Jira API token
        decrypted_token = decrypt_token(current_user.jira_api_token)

        # Create JiraClient with user's credentials
        return JiraClient(
            base_url=current_user.jira_base_url,
            email=current_user.jira_email,
            api_token=decrypted_token
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inicializar cliente de Jira: {str(e)}"
        )
