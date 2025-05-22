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
