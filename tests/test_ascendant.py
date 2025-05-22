import os
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Test data
TEST_API_KEY = "test_api_key"


@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"API_KEY": TEST_API_KEY}):
        yield


@pytest.fixture
def client():
    return TestClient(app)


def test_get_ascendant_basic(client):
    """Test getting ascendant for a specific time and location"""
    test_data = {
        "date_time": "2024-03-20T12:00:00",
        "latitude": 40.7128,  # New York
        "longitude": -74.0060,
    }

    response = client.post(
        "/ascendant", json=test_data, headers={"API_KEY": TEST_API_KEY}
    )
    assert response.status_code == 200
    data = response.json()

    # Check response structure
    assert "sign" in data
    assert "degrees" in data
    assert "debug" in data

    # Check debug information
    assert "input_datetime" in data["debug"]
    assert "datetime_utc" in data["debug"]
    assert "longitude" in data["debug"]
    assert "latitude" in data["debug"]
    assert "ascendant" in data["debug"]

    # Verify data types
    assert isinstance(data["sign"], str)
    assert isinstance(data["degrees"], float)
    assert 0 <= data["degrees"] < 30


def test_get_ascendant_with_timezone(client):
    """Test getting ascendant with timezone offset"""
    test_data = {
        "date_time": "2024-03-20T12:00:00",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "tz_offset": "-04:00",  # EDT
    }

    response = client.post(
        "/ascendant", json=test_data, headers={"API_KEY": TEST_API_KEY}
    )
    assert response.status_code == 200
    data = response.json()

    # Verify the UTC conversion in debug info
    assert data["debug"]["datetime_utc"] == "2024-03-20 16:00:00"


def test_get_ascendant_invalid_input(client):
    """Test getting ascendant with invalid input"""
    # Test invalid date format
    response = client.post(
        "/ascendant",
        json={
            "date_time": "invalid-date",
            "latitude": 40.7128,
            "longitude": -74.0060,
        },
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 422

    # Test invalid coordinates
    response = client.post(
        "/ascendant",
        json={
            "date_time": "2024-03-20T12:00:00",
            "latitude": 200,  # Invalid latitude
            "longitude": -74.0060,
        },
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 422


def test_get_ascendant_missing_required_fields(client):
    """Test getting ascendant with missing required fields"""
    # Test missing latitude
    response = client.post(
        "/ascendant",
        json={"date_time": "2024-03-20T12:00:00", "longitude": -74.0060},
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 422

    # Test missing longitude
    response = client.post(
        "/ascendant",
        json={"date_time": "2024-03-20T12:00:00", "latitude": 40.7128},
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 422
