from setuptools import setup, find_packages

__version__ = "1.0.0"
__author__ = "G Kiran"
__license__ = "MIT"

# Setup for pip installation
setup(
    name="digipin",
    version=__version__,
    author=__author__,
    author_email="goki75@gmail.com",
    description="A Python implementation of the DIGIPIN geocoding system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/goki75/digipin",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.1',
)
