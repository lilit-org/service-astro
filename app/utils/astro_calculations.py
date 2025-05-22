import re
from datetime import timedelta, timezone

########################################################
#           Constants
########################################################
SIGNS = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

ROUND_DECIMALS = 4


########################################################
#           Helper Functions
########################################################
def get_zodiac_sign(longitude: float) -> tuple[str, float]:
    sign_num = int(longitude / 30)
    degrees = longitude % 30
    return SIGNS[sign_num], degrees


def parse_tz_offset(tz_offset: str) -> timezone:
    match = re.match(r"([+-])(\d{2}):(\d{2})", tz_offset)
    if not match:
        raise ValueError("Invalid tz_offset format. Use +HH:MM or -HH:MM.")
    sign, hours, minutes = match.groups()
    delta = timedelta(hours=int(hours), minutes=int(minutes))
    return timezone(-delta if sign == "-" else delta)
