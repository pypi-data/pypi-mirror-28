from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='get_hubway_data',
    version='1.1',
    description='Extract data from Hubway CSVs',
    long_description=long_description,
    py_modules=["get_hubway_data"],
    install_requires=['matplotlib', 'pandas']
)
