import ephem
from fastapi import APIRouter

from app.models import AscendantResponse, LocationRequest
from app.routers.planets import ROUND_DECIMALS, get_zodiac_sign

router = APIRouter()


@router.post("/ascendant", response_model=AscendantResponse)
async def get_ascendant(request: LocationRequest):
    observer = ephem.Observer()
    observer.date = request.date_time
    observer.lat = str(request.latitude)
    observer.lon = str(request.longitude)
    sidereal_time = observer.sidereal_time() * 180 / ephem.pi

    # calculate the ascendant
    # the formula is: Ascendant = arctan(cos(obliquity) * sin(sidereal_time) /
    # (cos(sidereal_time) * cos(latitude) - sin(obliquity) * sin(latitude)))
    obliquity = ephem.Ecliptic(ephem.Sun()).lon * 180 / ephem.pi
    cos_obl = ephem.cos(obliquity)
    sin_obl = ephem.sin(obliquity)
    cos_lat = ephem.cos(request.latitude)
    sin_lat = ephem.sin(request.latitude)
    cos_sid = ephem.cos(sidereal_time)
    sin_sid = ephem.sin(sidereal_time)

    numerator = cos_obl * sin_sid
    denominator = cos_sid * cos_lat - sin_obl * sin_lat

    ascendant = ephem.degrees(ephem.atan2(numerator, denominator))
    if ascendant < 0:
        ascendant += 360

    sign, degrees = get_zodiac_sign(ascendant)

    return AscendantResponse(sign=sign, degrees=round(degrees, ROUND_DECIMALS))
