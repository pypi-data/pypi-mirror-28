#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup

sys.path.insert(0, os.path.dirname(__file__))
from jschema.version import __version__

setup(
    name="jschema",
    version=__version__,
    description="json schema tookit",
    license="MIT",
    author="Stepan Perlov",
    author_email="stepanperlov@gmail.com",
    url="https://github.com/stepan-perlov/jschema",
    install_requires=["PyYAML", "jinja2"],
    packages=["jschema", "jschema.formats", "jschema.node"],
    package_data={"jschema.formats": ["templates/*.j2"]},
    entry_points={
        "console_scripts": [
            "jschema = jschema.main:main"
        ]
    },
    platforms=["linux"]
)
