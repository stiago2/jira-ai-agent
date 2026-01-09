"""
Custom exceptions for the application.
"""


class BaseAppException(Exception):
    """Base exception for all application exceptions."""

    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class JiraAPIException(BaseAppException):
    """Exception raised when Jira API calls fail."""
    pass


class AIProcessingException(BaseAppException):
    """Exception raised when AI/LLM processing fails."""
    pass


class ValidationException(BaseAppException):
    """Exception raised when data validation fails."""
    pass


class ConfigurationException(BaseAppException):
    """Exception raised when configuration is invalid."""
    pass


class RateLimitException(BaseAppException):
    """Exception raised when rate limit is exceeded."""
    pass


class AuthenticationException(BaseAppException):
    """Exception raised when authentication fails."""
    pass


class ResourceNotFoundException(BaseAppException):
    """Exception raised when a resource is not found."""
    pass
