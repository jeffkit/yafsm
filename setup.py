#!/usr/bin/env python

from setuptools import setup, find_packages
from yafsm import version

url="https://github.com/jeffkit/yafsm/"

long_description="Yeah! Another Finite State Machine"

setup(name="yafsm",
      version=version,
      description=long_description,
      maintainer="jeff kit",
      maintainer_email="jeff@toraysoft.com",
      url = url,
      long_description=long_description,
      py_modules=['yafsm'],
     )


