"""
DIGIPIN Python Implementation

This module provides a function to generate a DIGIPIN, an alphanumeric string representation
of a location's latitude and longitude.

Author: Your Name
License: MIT
"""

from setuptools import setup, find_packages

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

def Get_DIGIPIN(lat, lon):
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
            if Lvl in {3, 6}:
                vDIGIPIN += "-"

        MinLat, MaxLat, MinLon, MaxLon = NextLvlMinLat, NextLvlMaxLat, NextLvlMinLon, NextLvlMaxLon

    return vDIGIPIN

if __name__ == "__main__":
    # Example usage
    try:
        latitude = 15.5
        longitude = 65.7
        digipin = Get_DIGIPIN(latitude, longitude)
        print(f"DIGIPIN for ({latitude}, {longitude}): {digipin}")
    except ValueError as e:
        print(e)

# Setup for pip installation
setup(
    name="digipin",
    version=__version__,
    author=__author__,
    author_email="your.email@example.com",
    description="A Python implementation of the DIGIPIN geocoding system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/digipin-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
