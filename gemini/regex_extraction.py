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
    if direction in ['S']:
        decimal_degrees *= -1
        
    return decimal_degrees

# --- Usage Example with your messy string ---
# Your scraping likely returns a combined string like "38°17′37.3″S 176°47′32.5″E"
raw_coord = "38°17′37.3″S 176°47′32.5″E"

# 1. Split Lat and Long (usually separated by space or non-breaking space)
# We can regex find both parts

    # Output: -38.29369..., 176.79236...

def convert_cords(coord_string: str) -> Tuple[float, float]:
    if not coord_string:
        return ""

    # This regex looks for:
    # 1. A number (possibly decimal)
    # 2. Any characters that aren't a letter (the degrees/minutes/seconds)
    # 3. A Direction letter (N, S, E, or W)
    pattern = r"(\d+(?:\.\d+)?[^NSEW]*[NSEW])"
    
    # Use findall to get ALL matches in the string
    matches = re.findall(pattern, coord_string)

    # Wikipedia strings often have the coordinates TWICE (DMS format and Decimal format)
    # e.g., "44°S 176°W / 44.0°S 176.3°W"
    # We only need the first two matches (Lat and Lon)
    if len(matches) >= 2:
        try:
            lat = parse_dms(matches[0])
            lon = parse_dms(matches[1])
            return (lat, lon)
        except Exception:
            return ""
            
    return ""
if __name__ == "__main__":
    print(convert_cords(raw_coord))
    print(convert_cords("44°2′13″S176°23′0″W� / �44.03694°S 176.38333°W� /-44.03694 "))
    print(convert_cords("38°38′00″S176°34′41″E﻿ / ﻿38.633332°S 176.578077°E﻿ /-38.633332; 176.578077﻿ (Wheao hydroelectric power station)"))