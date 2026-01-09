"""
Validators for Jira data.
"""

from app.core.exceptions import ValidationException


class JiraValidator:
    """Validator for Jira data."""

    @staticmethod
    def validate_summary(summary: str) -> None:
        """
        Validate Jira issue summary.

        Args:
            summary: Issue summary text

        Raises:
            ValidationException: If summary is invalid
        """
        # TODO: Implement validation logic
        if not summary or len(summary) > 255:
            raise ValidationException("Invalid summary")

    @staticmethod
    def validate_priority(priority: str) -> None:
        """
        Validate Jira priority.

        Args:
            priority: Priority value

        Raises:
            ValidationException: If priority is invalid
        """
        # TODO: Implement validation logic
        pass

    @staticmethod
    def validate_issue_type(issue_type: str) -> None:
        """
        Validate Jira issue type.

        Args:
            issue_type: Issue type value

        Raises:
            ValidationException: If issue type is invalid
        """
        # TODO: Implement validation logic
        pass

    @staticmethod
    def validate_project_key(project_key: str) -> None:
        """
        Validate Jira project key format.

        Args:
            project_key: Project key

        Raises:
            ValidationException: If project key is invalid
        """
        # TODO: Implement validation logic
        pass

    @staticmethod
    def sanitize_text(text: str) -> str:
        """
        Sanitize text for Jira.

        Args:
            text: Input text

        Returns:
            Sanitized text
        """
        # TODO: Implement sanitization logic
        return text.strip() if text else text
