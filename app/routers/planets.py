import ephem
from fastapi import APIRouter
from datetime import datetime
from app.models import DateTimeRequest, PlanetaryPositionsResponse, PlanetPosition


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

router = APIRouter()


def get_zodiac_sign(longitude: float) -> tuple[str, float]:

    sign_num = int(longitude / 30)
    degrees = longitude % 30
    return SIGNS[sign_num], degrees


@router.get("/planets", response_model=PlanetaryPositionsResponse)
@router.post("/planets", response_model=PlanetaryPositionsResponse)
async def get_planetary_positions(request: DateTimeRequest = None):

    date_time = request.date_time if request and request.date_time else datetime.now()
    observer = ephem.Observer()
    observer.date = date_time

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
        sign, degrees = get_zodiac_sign(ephem.Ecliptic(planet).lon * 180 / ephem.pi)
        results[name] = PlanetPosition(sign=sign, degrees=round(degrees, 2))

    return results
