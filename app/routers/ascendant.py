from datetime import timezone
from typing import Any

import swisseph as swe
from fastapi import APIRouter

from app.models import LocationRequest
from app.routers.planets import ROUND_DECIMALS, get_zodiac_sign
from app.utils.astro_calculations import parse_tz_offset

router = APIRouter()


@router.post("/ascendant", response_model=Any)
async def get_ascendant(request: LocationRequest) -> dict[str, Any]:
    dt = request.date_time
    if request.tz_offset:
        tz = parse_tz_offset(request.tz_offset)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz)
        dt = dt.astimezone(timezone.utc).replace(tzinfo=None)

    jd_ut = swe.julday(
        dt.year, dt.month, dt.day, dt.hour + dt.minute / 60 + dt.second / 3600
    )
    _, ascmc = swe.houses(jd_ut, request.latitude, request.longitude, b"A")
    ascendant = ascmc[0]
    sign, degrees = get_zodiac_sign(ascendant)

    return {
        "sign": sign,
        "degrees": round(degrees, ROUND_DECIMALS),
        "debug": {
            "input_datetime": str(request.date_time),
            "datetime_utc": str(dt),
            "longitude": request.longitude,
            "latitude": request.latitude,
            "ascendant": ascendant,
        },
    }
