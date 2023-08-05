#!/usr/bin/env python
from setuptools import setup, find_packages
#from distutils.core import setup

setup(
        name = "gotossh",
        version = "0.0.1",
        keywords = ("quick", "goto", "ssh"),
        description = "jump to ssh server quickly",
        license = "MIT License",
        install_requires = ["argcomplete"],
        url = "http://github.com/CuberL/goto",
        author = "cuberl",
        author_email = "me@cuberl.com",
        platforms = "any",
        packages = ['gotossh'],
        package_data = {
            "gotossh": ["bin/gotossh"]
        },
        entry_points = {
            "console_scripts": [
                "gotossh-init=gotossh:init",
                "gotossh-edit=gotossh:edit"
            ]
        }
)
