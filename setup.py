# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="co2tools",
    version="0.0.1",
    description="Easily automate generating 3D models from DWG files and merge DWG files for CO2 laser cutting",
    license="MIT",
    author="Mambix Ltd.",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
