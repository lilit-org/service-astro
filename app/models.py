from pydantic import BaseModel
from datetime import datetime
from typing import Dict


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
