"""
DIGIPIN Python Implementation

This module provides a function to encode and decode a DIGIPIN, an alphanumeric string 
representation of a location's latitude and longitude. 

Author: GOKI
License: MIT
"""

def encode(lat, lon):
    """
    Generate a DIGIPIN for the given latitude and longitude.

    DIGIPIN is a geocoding system that encodes latitude and longitude into an alphanumeric string.

    Args:
        lat (float): Latitude of the location. Must be in the range 1.50 to 39.00.
        lon (float): Longitude of the location. Must be in the range 63.50 to 99.00.

    Returns:
        str: The generated DIGIPIN, or an empty string if the inputs are out of range.

    Raises:
        ValueError: If the latitude or longitude is not within the valid range.
    """
    L1 = [list(l) for l in '0200,3456,G87M,J9KL'.split(',')]
    L2 = [list(l) for l in 'JG98,K327,L456,MPWX'.split(',')]
    vDIGIPIN = ''
    MinLat, MaxLat, MinLon, MaxLon = 1.50, 39.00, 63.50, 99.00
    LatDivBy, LonDivBy, LatDivDeg, LonDivDeg = 4, 4, 0, 0

    if lat < MinLat or lat > MaxLat or lon < MinLon or lon > MaxLon:
        raise ValueError(
            f"Input coordinates out of range. Latitude must be between {MinLat} and {MaxLat}, "
            f"Longitude must be between {MinLon} and {MaxLon}."
        )

    for Lvl in range(1, 11):
        LatDivDeg = (MaxLat - MinLat) / LatDivBy
        LonDivDeg = (MaxLon - MinLon) / LonDivBy
        
        NextLvlMaxLat = MaxLat
        NextLvlMinLat = MaxLat - LatDivDeg
        
        for x in range(LatDivBy):
            if NextLvlMinLat <= lat < NextLvlMaxLat:
                r = x
                break
            NextLvlMaxLat = NextLvlMinLat
            NextLvlMinLat -= LatDivDeg

        NextLvlMinLon = MinLon
        NextLvlMaxLon = MinLon + LonDivDeg
        
        for x in range(LonDivBy):
            if NextLvlMinLon <= lon < NextLvlMaxLon:
                c = x
                break
            NextLvlMinLon = NextLvlMaxLon
            NextLvlMaxLon += LonDivDeg

        if Lvl == 1:
            if L1[r][c] == "0":
                return "Out of Bound"
            vDIGIPIN += L1[r][c]
        else:
            vDIGIPIN += L2[r][c]
            if Lvl in (3, 6):
                vDIGIPIN += "-"

        MinLat, MaxLat, MinLon, MaxLon = NextLvlMinLat, NextLvlMaxLat, NextLvlMinLon, NextLvlMaxLon

    return vDIGIPIN

def decode(DigiPin):
    DigiPin = DigiPin.replace('-', '')
    if len(DigiPin) != 10:
        return "Invalid DIGIPIN"

    L1=[list(l) for l in '0200,3456,G87M,J9KL'.split(',')]
    L2=[list(l) for l in 'JG98,K327,L456,MPWX'.split(',')]
    MinLat,MaxLat,MinLon,MaxLon = 1.50,39.00,63.50,99.00
    LatDivBy,LonDivBy,LatDivDeg,LonDivDeg = 4,4,0,0
    for Lvl in range(10): 
        ri,ci = -1,-1
        digipinChar = DigiPin[Lvl]
        LatDivVal = (MaxLat - MinLat) / LatDivBy
        LonDivVal = (MaxLon - MinLon) / LonDivBy
        f = 0
        if Lvl == 0:
            for r in range(LatDivBy):
                for c in range(LonDivBy):
                    if L1[r][c] == digipinChar:
                        ri, ci, f = r, c, 1
                        break
        else:
            for r in range(LatDivBy):
                for c in range(LonDivBy):
                    if L2[r][c] == digipinChar:
                        ri, ci, f = r, c, 1
                        break
        if f == 0:
            return 'Invalid DIGIPIN'
        Lat1 = MaxLat - (LatDivVal * (ri + 1))
        Lat2 = MaxLat - (LatDivVal * (ri))
        Lon1 = MinLon + (LonDivVal * ci)
        Lon2 = MinLon + (LonDivVal * (ci + 1))
        MinLat, MaxLat, MinLon, MaxLon = Lat1, Lat2, Lon1, Lon2

    cLat = (Lat2 + Lat1) / 2
    cLon = (Lon2 + Lon1) / 2
    return cLat,cLon

if __name__ == "__main__":
    # Example usage
    try:
        latitude = 15.5
        longitude = 65.7
        pin = encode(latitude, longitude)
        print(f"Encode DIGIPIN for ({latitude}, {longitude}): {pin}")
        latlon=decode(pin)
        print(f"Decode DIGIPIN {pin}:{latlon}")
    except ValueError as e:
        print(e)
