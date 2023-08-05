#!/usr/bin/env python3

from setuptools import setup

setup(
    name = "tqs_client",
    version = "0.6",
    py_modules = ["tqs"],
    setup_requires = ["wheel"],
    install_requires = ["requests"],
    python_requires = ">=3",
    description = "Tiny Queue Service Client",
    author = "Stefan Arentz",
    author_email = "stefan@arentz.ca",
    url = "https://github.com/st3fan/tqs-client",
)
