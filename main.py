from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import ephem
from typing import Dict, List

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
    date_time: datetime

class PlanetPosition(BaseModel):
    sign: str
    degrees: float

PlanetaryPositionsResponse = Dict[str, PlanetPosition]

def get_zodiac_sign(longitude: float) -> tuple[str, float]:
    """Convert longitude to zodiac sign and degrees within sign."""
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    sign_num = int(longitude / 30)
    degrees = longitude % 30
    return signs[sign_num], degrees

@app.get("/")
async def root():
    return {"message": "Welcome to the Astrological Calculations API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/planetary-positions", response_model=PlanetaryPositionsResponse)
async def get_planetary_positions(request: DateTimeRequest):
    """Calculate planetary positions for a given date and time."""
    date_time = request.date_time
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
