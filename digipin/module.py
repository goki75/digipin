"""
DIGIPIN Python Implementation 

This module provides functions to encode and decode a DIGIPIN, an alphanumeric string 
representation of a location's latitude and longitude. 

Author: G Kiran (GOKI) 
License: MIT
"""
# Predefine the character grids
L1 = ('0200','3456','G87M','J9KL')
L2 = ('JG98','K327','L456','MPWX')
# Create mappings for efficient decoding
L1_map = {L1[r][c]: (r, c) for r in range(4) for c in range(4)}
L2_map = {L2[r][c]: (r, c) for r in range(4) for c in range(4)}

def encode(lat, lon):
    """
    Generate a DIGIPIN for the given latitude and longitude.
    """
    try:
        # Constants
        MinLat, MaxLat, MinLon, MaxLon = 1.50, 39.00, 63.50, 99.00
        LatDivBy, LonDivBy = 4, 4

        # Validate input ranges
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            raise TypeError("Latitude and Longitude must be numbers.")

        if not (MinLat <= lat <= MaxLat and MinLon <= lon <= MaxLon):
            raise ValueError(
                f"Input coordinates out of range. Latitude must be between {MinLat} and {MaxLat}, "
                f"Longitude must be between {MinLon} and {MaxLon}."
            )

        vDIGIPIN = []
        for Lvl in range(1, 11):
            LatDivDeg = (MaxLat - MinLat) / LatDivBy
            LonDivDeg = (MaxLon - MinLon) / LonDivBy

            # Determine the row and column
            r = int((MaxLat - lat) // LatDivDeg)
            c = int((lon - MinLon) // LonDivDeg)

            if r >= LatDivBy or c >= LonDivBy or r < 0 or c < 0:
                raise RuntimeError("Unexpected error in grid calculation.")

            # Add the character to the DIGIPIN
            if Lvl == 1:
                char = L1[r][c]
                if char == "0":
                    return "Out of Bound"
                vDIGIPIN.append(char)
            else:
                vDIGIPIN.append(L2[r][c])
                if Lvl in (3, 6):
                    vDIGIPIN.append("-")

            # Update boundaries for the next level
            MaxLat, MinLat = MaxLat - r * LatDivDeg, MaxLat - (r + 1) * LatDivDeg
            MinLon, MaxLon = MinLon + c * LonDivDeg, MinLon + (c + 1) * LonDivDeg

        return ''.join(vDIGIPIN)

    except Exception as e:
        return f"Error during encoding: {e}"

def decode(DigiPin):
    """
    Decode a DIGIPIN to latitude and longitude.
    """
    try:
        # Constants
        MinLat, MaxLat, MinLon, MaxLon = 1.50, 39.00, 63.50, 99.00
        LatDivBy, LonDivBy = 4, 4

        if not isinstance(DigiPin, str):
            raise TypeError("DIGIPIN must be a string.")

        DigiPin = DigiPin.replace('-', '')
        if len(DigiPin) != 10:
            raise ValueError("Invalid DIGIPIN length. DIGIPIN must be 10 characters.")

        for Lvl, char in enumerate(DigiPin):
            # Lookup row and column
            if Lvl == 0:
                r, c = L1_map.get(char, (-1, -1))
            else:
                r, c = L2_map.get(char, (-1, -1))

            if r == -1 or c == -1:
                raise ValueError(f"Invalid character '{char}' in DIGIPIN.")

            LatDivVal = (MaxLat - MinLat) / LatDivBy
            LonDivVal = (MaxLon - MinLon) / LonDivBy

            # Update boundaries based on row and column
            MaxLat, MinLat = MaxLat - r * LatDivVal, MaxLat - (r + 1) * LatDivVal
            MinLon, MaxLon = MinLon + c * LonDivVal, MinLon + (c + 1) * LonDivVal

        # Calculate the center latitude and longitude
        cLat = (MinLat + MaxLat) / 2
        cLon = (MinLon + MaxLon) / 2
        return round(cLat, 6), round(cLon, 6)

    except Exception as e:
        return f"Error during decoding: {e}"

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
