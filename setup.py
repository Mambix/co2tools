# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'co2tools'
about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description="Easily automate generating 3D models from DXF files and merge DXF files for CO2 laser cutting",
    license="MIT",
    author="Mambix Ltd.",
    author_email="ledi.mambix@gmail.com",
    url="https://github.com/Mambix/co2tools",
    packages=find_packages(exclude=('tests')),
    scripts=['bin/co2tools'],
    entry_points={'console_scripts': ['co2tools=co2tools:main']},
    install_requires=['numpy', 'scipy', 'trimesh[easy]', 'ezdxf', 'networkx', 'PyYaml'],
    long_description=long_description,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Multimedia :: Graphics :: 3D Modeling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ]
)
