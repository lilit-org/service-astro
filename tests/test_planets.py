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


def test_get_planets_current_time(client):
    """Test getting planetary positions for current time"""
    response = client.post("/planets", headers={"API_KEY": TEST_API_KEY})
    assert response.status_code == 200
    data = response.json()

    # Check that all planets are present
    expected_planets = [
        "Sun",
        "Moon",
        "Mercury",
        "Venus",
        "Mars",
        "Jupiter",
        "Saturn",
        "Uranus",
        "Neptune",
        "Pluto",
    ]
    assert all(planet in data for planet in expected_planets)

    # Check structure of each planet's data
    for planet_data in data.values():
        assert "sign" in planet_data
        assert "degrees" in planet_data
        assert isinstance(planet_data["degrees"], float)
        assert 0 <= planet_data["degrees"] < 30


def test_get_planets_specific_time(client):
    """Test getting planetary positions for a specific time"""
    test_time = "2024-03-20T12:00:00"
    response = client.post(
        "/planets",
        json={"date_time": test_time},
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 200
    data = response.json()

    # Verify we got data for all planets
    assert len(data) == 10

    # Check that the data structure is correct
    for planet, position in data.items():
        assert isinstance(position, dict)
        assert "sign" in position
        assert "degrees" in position
        assert position["sign"] in [
            "Aries",
            "Taurus",
            "Gemini",
            "Cancer",
            "Leo",
            "Virgo",
            "Libra",
            "Scorpio",
            "Sagittarius",
            "Capricorn",
            "Aquarius",
            "Pisces",
        ]
        assert 0 <= position["degrees"] < 30


def test_get_planets_invalid_time(client):
    """Test getting planetary positions with invalid time format"""
    response = client.post(
        "/planets",
        json={"date_time": "invalid-time"},
        headers={"API_KEY": TEST_API_KEY},
    )
    assert response.status_code == 422  # Validation error


def test_get_zodiac_sign():
    """Test the zodiac sign calculation function"""
    from app.routers.planets import get_zodiac_sign

    # Test some known positions
    assert get_zodiac_sign(0) == ("Aries", 0)
    assert get_zodiac_sign(30) == ("Taurus", 0)
    assert get_zodiac_sign(45) == ("Taurus", 15)
    assert get_zodiac_sign(359) == ("Pisces", 29)
