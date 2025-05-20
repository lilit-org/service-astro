from fastapi import APIRouter
from datetime import datetime
import ephem
from app.models import DateTimeRequest, PlanetaryPositionsResponse, PlanetPosition
from app.utils import get_zodiac_sign

router = APIRouter()

@router.get("/planetary-positions", response_model=PlanetaryPositionsResponse)
@router.post("/planetary-positions", response_model=PlanetaryPositionsResponse)
async def get_planetary_positions(request: DateTimeRequest = None):
    """Calculate planetary positions for a given date and time. If no date/time is provided, uses current time."""
    date_time = request.date_time if request and request.date_time else datetime.now()
    observer = ephem.Observer()
    observer.date = date_time

    # List of planets to calculate
    planets = {
        "Sun": ephem.Sun(),
        "Moon": ephem.Moon(),
        "Mercury": ephem.Mercury(),
        "Venus": ephem.Venus(),
        "Mars": ephem.Mars(),
        "Jupiter": ephem.Jupiter(),
        "Saturn": ephem.Saturn(),
        "Uranus": ephem.Uranus(),
        "Neptune": ephem.Neptune(),
        "Pluto": ephem.Pluto()
    }

    results = {}
    for name, planet in planets.items():
        planet.compute(observer)
        # Convert longitude to zodiac sign and degrees
        sign, degrees = get_zodiac_sign(ephem.Ecliptic(planet).lon * 180 / ephem.pi)
        results[name] = PlanetPosition(sign=sign, degrees=round(degrees, 2))

    return results
