"""
Response models for API endpoints.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

from app.models.jira import JiraIssueType, JiraPriority


class TaskCreatedResponse(BaseModel):
    """Response model for successfully created task."""

    success: bool = True
    issue_key: str
    issue_url: str
    summary: str
    priority: JiraPriority
    issue_type: JiraIssueType
    created_at: datetime


class TaskPreviewResponse(BaseModel):
    """Response model for task preview."""

    summary: str
    description: str
    priority: JiraPriority
    issue_type: JiraIssueType
    confidence: float = Field(ge=0.0, le=1.0)
    suggestions: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    jira_connected: bool
    ai_service_ready: bool
    timestamp: datetime


class MetadataResponse(BaseModel):
    """Metadata response for Jira configuration."""

    projects: list
    issue_types: list
    priorities: list
