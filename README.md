# DIGIPIN Python Implementation - Unofficial Version

DIGIPIN is a geocoding system developed by India Post in collaboration with IIT Hyderabad. It divides India's geographical territory into uniform 4-meter by 4-meter units, assigning each a unique 10-character alphanumeric code derived from latitude and longitude coordinates. This system enhances address precision, facilitating efficient delivery of public and private services across India.
## Features
- **Generate DIGIPIN**: Compute the DIGIPIN based on latitude and longitude inputs.
- **Input Validation**: Ensures latitude and longitude are within acceptable ranges.
- **Precision Levels**: Supports up to 10 levels of precision for detailed location encoding.
## Requirements
- Python 3.6 or later.
## Installation from GitHub
You can install this package directly from GitHub using pip:
```bash
pip install git+https://github.com/goki75/pydigipin.git
```
## Usage
### Encoding
Import the encode and/or decode function from the module and pass the latitude and longitude as arguments:

```python
from digipin import encode

try:
    dpin = encode(15.5, 65.7)
    print(f"DIGIPIN: {digipin}")
except ValueError as e:
    print(e)
```
####  Output

```bash
DIGIPIN: GL8-874-X3GW
```
### Decoding
```python
from digipin import decode
try:
    latlon = decode('GL8-874-X3GW')
    print(f"(Lat,Long): {latlon}")
except Error as e:
    print(e)
```
####  Output

```bash
(Lat,Long): (15.5, 65.70001)
```

## Input Constraints

- **Latitude Range**: 1.50 to 39.00
- **Longitude Range**: 63.50 to 99.00

If the inputs are out of range, the function raises a `ValueError` with an appropriate message.

# What is DIGIPIN? 

The Department of Posts also know as India Post is undertaking a project to establish a standardized, nationwide geo-coded addressing system by developing a National level Grid known as DIGIPIN.
The implementation of this Digital Addressing system would ensure simplified addressing solutions for citizen centric delivery of public and private services. A standardized geo-coded addressing system would enhance India’s geo-spatial structure. It would add to the geospatial knowledge stack of the country in line with the National Geospatial Policy 2022, which seeks to strengthen the geospatial sector to support national development, economic prosperity and a thriving information economy.

## Understanding DIGIPIN

DIGIPIN is an alphanumeric offline grid system that divides India's geographical territory into uniform 4-meter by 4-meter units. Each unit is assigned a unique 10-character alphanumeric code derived from its latitude and longitude coordinates. This system provides precise location-based identification, especially useful in areas with unstructured or changing addresses.

## Contributing

Feel free to fork the repository and submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

For more information about DIGIPIN, visit [mydigipin.com](https://www.mydigipin.com/p/digipin.html).

This expanded documentation provides a detailed overview of DIGIPIN, its purpose, and how to use the Python implementation. 
