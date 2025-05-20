import ephem
import requests

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

def get_zodiac_sign(longitude: float) -> tuple[str, float]:
    """Convert longitude to zodiac sign and degrees within sign."""
    sign_num = int(longitude / 30)
    degrees = longitude % 30
    print(f"Longitude: {longitude}, Sign number: {sign_num}, Sign: {SIGNS[sign_num]}, Degrees: {degrees}")
    return SIGNS[sign_num], degrees

def get_ascendant_from_lst(lst_hours, latitude_deg):
    # Use ephem to convert LST and latitude to the ascendant
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