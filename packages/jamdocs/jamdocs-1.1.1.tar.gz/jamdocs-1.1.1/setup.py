#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from setuptools import setup

setup(
    name="jamdocs",
    version="1.1.1",
    description="IchigoJam Docs",
    long_description="This would greatly encourage you when you totally have no idea of how to use the embeded BASIC language in IchigoJam. w",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Basic"
    ],
    keywords="ichigojam docs",
    author="Cocoa Oikawa",
    author_email="cocoaoikawa@meowtain.edu.pl",
    license="MIT",
    packages=["jamdocs"],
    package_dir={"jamdocs": "jamdocs"},
    package_data={"jamdocs": ["docs/ichigojam.zip"]},
    url = "https://github.com/BlueCocoa/jam",
    include_package_data=True,
    zip_safe=False,
    scripts=["jamdocs/bin/jamdocs"]
)
