"""
Task orchestrator that coordinates AI and Jira services.
"""

from datetime import datetime
from typing import Dict, Any, Optional

from app.core.logging import logger
from app.models.jira import JiraIssue, JiraIssueType, JiraPriority
from app.models.responses import TaskCreatedResponse, TaskPreviewResponse
from app.services.jira_service import JiraService
from app.services.ai_service import AIService


class TaskOrchestrator:
    """
    Orchestrates the flow of creating Jira tasks from natural language.
    """

    def __init__(self, jira_service: JiraService, ai_service: AIService):
        """
        Initialize orchestrator with required services.

        Args:
            jira_service: Jira service instance
            ai_service: AI service instance
        """
        self.jira_service = jira_service
        self.ai_service = ai_service

    async def create_task_from_natural_language(
        self,
        text: str,
        project_key: str,
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> TaskCreatedResponse:
        """
        Create a Jira task from natural language text.

        Args:
            text: Natural language description of the task
            project_key: Jira project key
            user_preferences: Optional user preferences

        Returns:
            TaskCreatedResponse with created issue details
        """
        logger.info(f"Creating task from natural language for project {project_key}")

        # Step 1: Parse text with AI
        # TODO: Implement full parsing logic
        parsed_data = await self.ai_service.parse_task_from_text(text)

        # Step 2: Validate extracted data
        # TODO: Implement validation

        # Step 3: Build Jira issue
        issue = JiraIssue(
            project_key=project_key,
            summary=parsed_data["summary"],
            description=parsed_data["description"],
            issue_type=JiraIssueType(parsed_data["issue_type"]),
            priority=JiraPriority(parsed_data["priority"])
        )

        # Step 4: Apply user preferences
        # TODO: Implement preferences logic

        # Step 5: Validate project access
        # TODO: Implement access validation

        # Step 6: Create issue in Jira
        created_issue = await self.jira_service.create_issue(issue)

        # Step 7: Build response
        response = TaskCreatedResponse(
            success=True,
            issue_key=created_issue.key,
            issue_url=created_issue.browse_url,
            summary=issue.summary,
            priority=issue.priority,
            issue_type=issue.issue_type,
            created_at=datetime.utcnow()
        )

        return response

    async def preview_task_from_natural_language(
        self,
        text: str,
        project_key: str
    ) -> TaskPreviewResponse:
        """
        Preview how a task will be created without actually creating it.

        Args:
            text: Natural language description of the task
            project_key: Jira project key

        Returns:
            TaskPreviewResponse with preview details
        """
        logger.info(f"Generating task preview for project {project_key}")

        # Parse text with AI
        parsed_data = await self.ai_service.parse_task_from_text(text)

        # TODO: Implement suggestions logic

        return TaskPreviewResponse(
            summary=parsed_data["summary"],
            description=parsed_data["description"],
            priority=JiraPriority(parsed_data["priority"]),
            issue_type=JiraIssueType(parsed_data["issue_type"]),
            confidence=parsed_data.get("confidence", 0.0),
            suggestions=None
        )
