"""
Pytest configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_task_text():
    """Sample task text for testing."""
    return "Create a high priority task to implement OAuth2 authentication"


@pytest.fixture
def sample_project_key():
    """Sample project key for testing."""
    return "PROJ"
