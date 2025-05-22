from datetime import datetime
from typing import Dict

from pydantic import BaseModel, Field


class DateTimeRequest(BaseModel):
    date_time: datetime | None = None


class LocationRequest(BaseModel):
    date_time: datetime
    latitude: float = Field(
        ge=-90, le=90, description="Latitude in degrees (-90 to 90)"
    )
    longitude: float = Field(
        ge=-180, le=180, description="Longitude in degrees (-180 to 180)"
    )
    tz_offset: str | None = None


class PlanetPosition(BaseModel):
    sign: str
    degrees: float


class AscendantResponse(BaseModel):
    sign: str
    degrees: float


PlanetaryPositionsResponse = Dict[str, PlanetPosition]
