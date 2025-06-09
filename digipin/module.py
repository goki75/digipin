#merged
"""
DIGIPIN Python Implementation 

This module provides functions to encode and decode a DIGIPIN, an alphanumeric string 
representation of a location's latitude and longitude. 

Author: G Kiran (GOKI) 
License: MIT

2025-06-06: Updated as per https://github.com/CEPT-VZG/digipin/blob/main/src/digipin.js
"""
GRID = ["FC98", "J327", "K456", "LMPT"]
BOUNDS = {"minLat": 2.5, "maxLat": 38.5, "minLon": 63.5, "maxLon": 99.5 }

def encode(lat, lon):
    if lat < BOUNDS['minLat'] or lat > BOUNDS['maxLat']:
        raise ValueError('Latitude out of range')
    if lon < BOUNDS['minLon'] or lon > BOUNDS['maxLon']:
        raise ValueError('Longitude out of range')

    min_lat, max_lat  = BOUNDS['minLat'],BOUNDS['maxLat']
    min_lon, max_lon = BOUNDS['minLon'], BOUNDS['maxLon']
    digipin = ''

    for level in range(1, 11):
        lat_div = (max_lat - min_lat) / 4
        lon_div = (max_lon - min_lon) / 4

        # REVERSED row logic (to match original)
        row = 3 - int((lat - min_lat) // lat_div)
        col =int((lon - min_lon) // lon_div)

        row = max(0, min(row, 3))
        col = max(0, min(col, 3))

        digipin += GRID[row][col]

        if level == 3 or level == 6:
            digipin += '-'

        # Update bounds (reverse logic for row)
        max_lat = min_lat + lat_div * (4 - row)
        min_lat = min_lat + lat_div * (3 - row)

        min_lon = min_lon + lon_div * col
        max_lon = min_lon + lon_div

    return digipin

def decode(digipin):
    pin = digipin.upper().replace('-', '')
    if len(pin) != 10:
        raise ValueError("Invalid DIGIPIN")

    min_lat, max_lat = BOUNDS["minLat"], BOUNDS["maxLat"]
    min_lon, max_lon = BOUNDS["minLon"], BOUNDS["maxLon"]

    for char in pin:
        found = False
        for r in range(4):
            if char in GRID[r]:
                c = GRID[r].index(char)
                found = True
                break
        if not found:
            raise ValueError("Invalid character in DIGIPIN")

        lat_div = (max_lat-min_lat)/4
        lon_div = (max_lon-min_lon)/4

        max_lat = max_lat-lat_div*r
        min_lat = max_lat-lat_div
        min_lon = min_lon+lon_div*c
        max_lon = min_lon+lon_div

    lat = round((min_lat+max_lat)/2,6)
    lon = round((min_lon+max_lon)/2,6)
    return lat,lon

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
