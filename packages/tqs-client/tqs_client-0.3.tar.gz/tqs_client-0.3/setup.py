#!/usr/bin/env python3

from setuptools import setup

setup_requires = [
    "wheel",
]

install_requires = [
    "requests",
]

setup(
    name = "tqs_client",
    version = "0.3",
    packages = ["tqs"],
    #
    setup_requires = setup_requires,
    install_requires = install_requires,
    python_requires = "~=3.6",
    #
    description = "Tiny Queue Service Client",
    author = "Stefan Arentz",
    author_email = "stefan@arentz.ca",
    url = "https://github.com/st3fan/tqs-client",
)
