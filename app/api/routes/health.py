"""
Health check endpoints.
"""

from datetime import datetime
from fastapi import APIRouter

from app.models.responses import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthResponse with service status
    """
    # TODO: Implement actual health checks
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        jira_connected=False,  # TODO: Check actual Jira connectivity
        ai_service_ready=False,  # TODO: Check AI service readiness
        timestamp=datetime.utcnow()
    )
