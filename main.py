from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import ephem
from typing import Dict, List
import math
import swisseph as swe
import kerykeion as kr
import pytz
from flatlib.chart import Chart
from flatlib.datetime import Datetime as FlatlibDatetime
from flatlib.geopos import GeoPos
import requests

app = FastAPI(
    title="Astrological Calculations API",
    description="API for performing astrological calculations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DateTimeRequest(BaseModel):
    date_time: datetime | None = None

class LocationRequest(BaseModel):
    date_time: datetime
    latitude: float
    longitude: float
    tz_offset: str | None = None

class PlanetPosition(BaseModel):
    sign: str
    degrees: float

class AscendantResponse(BaseModel):
    sign: str
    degrees: float

PlanetaryPositionsResponse = Dict[str, PlanetPosition]

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_zodiac_sign(longitude: float) -> tuple[str, float]:
    """Convert longitude to zodiac sign and degrees within sign."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_num = int(longitude / 30)
    degrees = longitude % 30
    print(f"Longitude: {longitude}, Sign number: {sign_num}, Sign: {signs[sign_num]}, Degrees: {degrees}")
    return signs[sign_num], degrees

@app.get("/")
async def root():
    return {"message": "Welcome to the Astrological Calculations API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/planetary-positions", response_model=PlanetaryPositionsResponse)
@app.post("/planetary-positions", response_model=PlanetaryPositionsResponse)
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

def get_ascendant_from_lst(lst_hours, latitude_deg):
    # Use ephem to convert LST and latitude to the ascendant
    # Set up a dummy observer at Greenwich, then set sidereal time and latitude
    obs = ephem.Observer()
    obs.lat = str(latitude_deg)
    obs.lon = '0'  # LST is independent of longitude
    obs.elev = 0
    obs.date = '2000/01/01 00:00:00'  # Dummy date
    obs.sidereal_time = lst_hours
    asc = ephem.Equatorial(0, 0, epoch=obs.date)
    asc_ecl = ephem.Ecliptic(asc, epoch=obs.date)
    asc_deg = asc_ecl.lon * 180 / ephem.pi
    sign_num = int(asc_deg // 30)
    degrees = asc_deg % 30
    return SIGNS[sign_num], degrees

def get_ascendant_divineapi(
    api_key: str,
    auth_token: str,
    full_name: str,
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    gender: str,
    place: str,
    lat: float,
    lon: float,
    tzone: float,
    house_system: str = "P"
):
    url = "https://astroapi-4.divineapi.com/western-api/v1/ascendant-report"
    payload = {
        'api_key': api_key,
        'full_name': full_name,
        'day': str(day),
        'month': str(month),
        'year': str(year),
        'hour': str(hour),
        'min': str(minute),
        'sec': str(second),
        'gender': gender,
        'place': place,
        'lat': str(lat),
        'lon': str(lon),
        'tzone': str(tzone),
        'house_system': house_system
    }
    headers = {
        'Authorization': f'Bearer {auth_token}'
    }
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

@app.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: LocationRequest):
    # Extract date and time components
    dt = request.date_time
    api_key = "YOUR_API_KEY"  # TODO: Replace with your actual API key
    auth_token = "YOUR_AUTH_TOKEN"  # TODO: Replace with your actual Auth token
    # You may want to pass these as environment variables for security
    result = get_ascendant_divineapi(
        api_key=api_key,
        auth_token=auth_token,
        full_name="Test User",
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
        gender="other",
        place="Zurich, Switzerland",  # You can make this dynamic
        lat=request.latitude,
        lon=request.longitude,
        tzone=2,  # You can make this dynamic
        house_system="P"
    )
    # Parse the response
    sign = result["data"]["sign"]
    degrees = float(result["data"]["full_degree"]) % 30
    return AscendantResponse(sign=sign, degrees=round(degrees, 2))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
