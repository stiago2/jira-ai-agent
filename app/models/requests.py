"""
Request models for API endpoints.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    """Request model for creating a task from natural language."""

    text: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Natural language text describing the task"
    )

    project_key: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Jira project key"
    )

    preferences: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional user preferences for task creation"
    )


class PreviewTaskRequest(BaseModel):
    """Request model for previewing a task without creating it."""

    text: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Natural language text describing the task"
    )

    project_key: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Jira project key"
    )
