"""
DIGIPIN Python Implementation 

This module provides functions to encode and decode a DIGIPIN, an alphanumeric string 
representation of a location's latitude and longitude. 

Author: G Kiran (GOKI) 
License: MIT

2025-06-06: Updated as per https://github.com/CEPT-VZG/digipin/blob/main/src/digipin.js
"""
import math
import re

REGEX_PATTERN_DIGIPIN = re.compile(r'^[2-9CFJKLMPT]{3}-[2-9CFJKLMPT]{3}-[2-9CFJKLMPT]{4}$')

DIGIPIN_GRID = [
    ['F', 'C', '9', '8'],
    ['J', '3', '2', '7'],
    ['K', '4', '5', '6'],
    ['L', 'M', 'P', 'T']
]

BOUNDS = {
    'minLat': 2.5,
    'maxLat': 38.5,
    'minLon': 63.5,
    'maxLon': 99.5
}

def validate_digipin(d):
    """Validates if a given string is a valid digipin. Should be in format like: 4FP-994-M7C6"""
    global REGEX_PATTERN_DIGIPIN
    return bool(REGEX_PATTERN_DIGIPIN.match(d))

def encode(lat, lon):
    if lat < BOUNDS['minLat'] or lat > BOUNDS['maxLat']:
        raise ValueError('Latitude out of range')
    if lon < BOUNDS['minLon'] or lon > BOUNDS['maxLon']:
        raise ValueError('Longitude out of range')

    min_lat = BOUNDS['minLat']
    max_lat = BOUNDS['maxLat']
    min_lon = BOUNDS['minLon']
    max_lon = BOUNDS['maxLon']

    digipin = ''

    for level in range(1, 11):
        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        # REVERSED row logic (to match original)
        row = 3 - math.floor((lat - min_lat) / lat_div)
        col = math.floor((lon - min_lon) / lon_div)

        row = max(0, min(row, 3))
        col = max(0, min(col, 3))

        digipin += DIGIPIN_GRID[row][col]

        if level == 3 or level == 6:
            digipin += '-'

        # Update bounds (reverse logic for row)
        max_lat = min_lat + lat_div * (4 - row)
        min_lat = min_lat + lat_div * (3 - row)

        min_lon = min_lon + lon_div * col
        max_lon = min_lon + lon_div

    return digipin

def decode(digipin):
    if not validate_digipin(digipin):
        raise ValueError('Invalid DIGIPIN')
        
    pin = digipin.replace('-', '')
    if len(pin) != 10:
        raise ValueError('Invalid DIGIPIN')
    
    min_lat = BOUNDS['minLat']
    max_lat = BOUNDS['maxLat']
    min_lon = BOUNDS['minLon']
    max_lon = BOUNDS['maxLon']

    for i in range(10):
        char = pin[i]
        found = False
        ri = -1
        ci = -1

        # Locate character in DIGIPIN grid
        for r in range(4):
            for c in range(4):
                if DIGIPIN_GRID[r][c] == char:
                    ri = r
                    ci = c
                    found = True
                    break
            if found:
                break

        if not found:
            raise ValueError('Invalid character in DIGIPIN')

        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        lat1 = max_lat - lat_div * (ri + 1)
        lat2 = max_lat - lat_div * ri
        lon1 = min_lon + lon_div * ci
        lon2 = min_lon + lon_div * (ci + 1)

        # Update bounding box for next level
        min_lat = lat1
        max_lat = lat2
        min_lon = lon1
        max_lon = lon2

    center_lat = round((min_lat + max_lat) / 2, 6)
    center_lon = round((min_lon + max_lon) / 2, 6)

    return center_lat, center_lon

if __name__ == "__main__":
    # Example usage
    try:
        latitude = 15.553
        longitude = 65.734
        pin = encode(latitude, longitude)
        print(f"Encode DIGIPIN for ({latitude}, {longitude}): {pin}")
        if isinstance(pin, str) and not pin.startswith("Error"):
            latlon = decode(pin)
            print(f"Decode DIGIPIN {pin}: {latlon}")
        else:
            print(pin)
    except ValueError as e:
        print(e)
