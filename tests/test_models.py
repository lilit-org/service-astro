from datetime import datetime

from app.models import (
    AscendantResponse,
    DateTimeRequest,
    LocationRequest,
    PlanetaryPositionsResponse,
    PlanetPosition,
)


def test_datetime_request():
    """Test DateTimeRequest model validation"""
    # Test with valid datetime
    valid_time = "2024-03-20T12:00:00"
    request = DateTimeRequest(date_time=datetime.fromisoformat(valid_time))
    assert request.date_time == datetime.fromisoformat(valid_time)

    # Test with None (default value)
    request = DateTimeRequest()
    assert request.date_time is None


def test_location_request():
    """Test LocationRequest model validation"""
    # Test with valid data
    valid_time = "2024-03-20T12:00:00"
    request = LocationRequest(
        date_time=datetime.fromisoformat(valid_time),
        latitude=40.7128,
        longitude=-74.0060,
        tz_offset="America/New_York",
    )
    assert request.date_time == datetime.fromisoformat(valid_time)
    assert request.latitude == 40.7128
    assert request.longitude == -74.0060
    assert request.tz_offset == "America/New_York"


def test_planet_position():
    """Test PlanetPosition model validation"""
    # Test with valid data
    position = PlanetPosition(sign="Aries", degrees=15.5)
    assert position.sign == "Aries"
    assert position.degrees == 15.5


def test_ascendant_response():
    """Test AscendantResponse model validation"""
    # Test with valid data
    response = AscendantResponse(sign="Taurus", degrees=20.5)
    assert response.sign == "Taurus"
    assert response.degrees == 20.5


def test_planetary_positions_response():
    """Test PlanetaryPositionsResponse type"""
    # Create a sample response
    response: PlanetaryPositionsResponse = {
        "Sun": PlanetPosition(sign="Aries", degrees=15.5),
        "Moon": PlanetPosition(sign="Taurus", degrees=20.5),
    }

    assert isinstance(response, dict)
    assert all(isinstance(pos, PlanetPosition) for pos in response.values())
    assert response["Sun"].sign == "Aries"
    assert response["Moon"].sign == "Taurus"
