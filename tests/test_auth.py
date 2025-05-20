import os
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.auth import (
    PUBLIC_PATHS,
    APIKeyMiddleware,
    failed_attempts,
    is_rate_limited,
    record_failed_attempt,
    request_counts,
)

# Test data
VALID_API_KEY = "test-api-key-123"
INVALID_API_KEY = "invalid-key"
TEST_IP = "127.0.0.1"


@pytest.fixture(autouse=True)
def reset_state():
    """Reset rate limiting and failed attempts state before each test"""
    request_counts.clear()
    failed_attempts.clear()
    yield


@pytest.fixture
def app():
    app = FastAPI()
    app.add_middleware(APIKeyMiddleware)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    @app.get("/docs")
    async def docs():
        return {"message": "API Documentation"}

    @app.get("/openapi.json")
    async def openapi():
        return {"openapi": "3.0.0"}

    @app.get("/planets")
    async def planets():
        return {"planets": ["Mercury", "Venus", "Earth"]}

    return app


@pytest.fixture
def client(app):
    return TestClient(app)


@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {"API_KEY": VALID_API_KEY}):
        yield


def test_public_paths_access(client):
    """Test that public paths are accessible without API key"""
    for path in PUBLIC_PATHS:
        response = client.get(path)
        assert response.status_code == 200


def test_api_key_validation(client, mock_env_vars):
    """Test API key validation"""
    # Test with valid API key in header
    response = client.get("/planets", headers={"API_KEY": VALID_API_KEY})
    assert response.status_code == 200

    # Test with invalid API key
    response = client.get("/planets", headers={"API_KEY": INVALID_API_KEY})
    assert response.status_code == 403

    # Test with valid API key in query params for /planets
    response = client.get(f"/planets?API_KEY={VALID_API_KEY}")
    assert response.status_code == 200


def test_rate_limiting():
    """Test rate limiting functionality"""
    # Test normal request
    assert not is_rate_limited(TEST_IP)

    # Test blocked IP
    for _ in range(5):
        record_failed_attempt(TEST_IP)
    assert is_rate_limited(TEST_IP)


def test_failed_attempts():
    """Test failed attempts tracking"""
    # Test normal failed attempt
    record_failed_attempt(TEST_IP)
    assert not is_rate_limited(TEST_IP)

    # Test multiple failed attempts
    for _ in range(5):
        record_failed_attempt(TEST_IP)

    # Should be rate limited after 5 failed attempts
    assert is_rate_limited(TEST_IP)


def test_api_key_middleware_initialization():
    """Test APIKeyMiddleware initialization"""
    # Test with single API key
    with patch.dict(os.environ, {"API_KEY": VALID_API_KEY}):
        middleware = APIKeyMiddleware(None)
        assert VALID_API_KEY in middleware.valid_api_keys

    # Test with multiple API keys
    multiple_keys = f"{VALID_API_KEY},another-key,third-key"
    with patch.dict(os.environ, {"API_KEYS": multiple_keys}):
        middleware = APIKeyMiddleware(None)
        assert len(middleware.valid_api_keys) == 3
        assert VALID_API_KEY in middleware.valid_api_keys
