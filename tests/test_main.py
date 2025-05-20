import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import MESSAGE, app

# Test data
TEST_API_KEY = "test_api_key"


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(
        os.environ,
        {
            "API_KEY": TEST_API_KEY,
            "ALLOWED_ORIGINS": "http://localhost:3000,http://localhost:8000",
            "CORS_MAX_AGE": "3600",
        },
    ):
        yield


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint returns the correct message"""
    response = client.get("/", headers={"API_KEY": TEST_API_KEY})
    assert response.status_code == 200
    assert response.json() == {"message": MESSAGE}
