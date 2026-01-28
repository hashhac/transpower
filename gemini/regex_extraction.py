import re
from typing import Tuple
def parse_dms(dms_str):
    """
    Parses a string like "38°17′37.3″S" into a decimal float like -38.2936.
    Handles variable whitespace and different types of quote marks.
    """
    if not dms_str:
        raise ValueError("This needs to be the case here")
        return None
        
    # Regex explanation:
    # (\d+(?:\.\d+)?)  -> Capture a number (integer or decimal)
    # [°\s]* -> Match degree symbol or space
    # ... repeated for minutes and seconds
    # ([NSEW])         -> Capture the direction letter
    
    # We look for 3 numbers (Deg, Min, Sec) usually, but sometimes only 2.
    # This pattern looks for the parts broadly.
    pattern = r"(\d+(?:\.\d+)?)[°\s]+(\d+(?:\.\d+)?)?[′'\s]+(\d+(?:\.\d+)?)?[″\"\s]*([NSEW])"
    
    match = re.search(pattern, dms_str)
    
    if not match:
        # Fallback: sometimes it's just decimal already "38.22 S"
        return None
    
    deg, min, sec, direction = match.groups()
    
    # Convert to floats, defaulting to 0 if parts are missing
    d = float(deg)
    m = float(min) if min else 0.0
    s = float(sec) if sec else 0.0
    
    # The Formula: Degrees + Minutes/60 + Seconds/3600
    decimal_degrees = d + (m / 60) + (s / 3600)
    
    # Handle Hemisphere
    if direction in ['S', 'W']:
        decimal_degrees *= -1
        
    return decimal_degrees

# --- Usage Example with your messy string ---
# Your scraping likely returns a combined string like "38°17′37.3″S 176°47′32.5″E"
raw_coord = "38°17′37.3″S 176°47′32.5″E"

# 1. Split Lat and Long (usually separated by space or non-breaking space)
# We can regex find both parts

    # Output: -38.29369..., 176.79236...

def convert_cords(convert_cords : str) -> Tuple[float,float]:
    '''
    Docstring for convert_cords
    
    :param raw_coord: Description
    :type raw_coord: str
    '''
    if convert_cords == "":
        return ""
    parts = re.findall(r"[\d\.]+[^NSEW]*[NSEW]", raw_coord)

    if len(parts) == 2:
        lat = parse_dms(parts[0])
        lon = parse_dms(parts[1])
        return lat,lon
    else:
        raise ValueError(f"Did not correctly convert data of {raw_coord}")