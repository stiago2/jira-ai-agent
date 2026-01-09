"""
Jira domain models.
"""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class JiraPriority(str, Enum):
    """Jira priority levels."""
    HIGHEST = "Highest"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    LOWEST = "Lowest"


class JiraIssueType(str, Enum):
    """Jira issue types."""
    TASK = "Task"
    STORY = "Story"
    BUG = "Bug"
    EPIC = "Epic"
    SUBTASK = "Sub-task"


class JiraProject(BaseModel):
    """Jira project model."""
    key: str
    name: str
    id: str
    description: Optional[str] = None


class JiraIssue(BaseModel):
    """Jira issue model for creation."""
    project_key: str
    summary: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    issue_type: JiraIssueType = JiraIssueType.TASK
    priority: JiraPriority = JiraPriority.MEDIUM
    assignee: Optional[str] = None
    labels: Optional[List[str]] = Field(default=[])

    class Config:
        use_enum_values = True


class JiraIssueCreated(BaseModel):
    """Response model for created Jira issue."""
    id: str
    key: str
    self: str

    @property
    def browse_url(self) -> str:
        """Get the browse URL for the issue."""
        base_url = self.self.split("/rest/api")[0]
        return f"{base_url}/browse/{self.key}"
