#!/usr/bin/env python
# coding=utf-8

import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements

install_requirements = parse_requirements('requirements.txt', session=uuid.uuid1())
requirements = [str(req.req) for req in install_requirements]

setup(
    name="python-unsplash-async",
    version="1.0.1",
    description="A Python client for the Unsplash API.",
    license="MIT",
    maintainer="Alin Panaitiu",
    maintainer_email="alin.p32@gmail.com",
    author="Yakup Adaklı",
    author_email="yakup.adakli@gmail.com",
    url="http://github.com/alin23/python-unsplash",
    packages=find_packages(exclude=["tests"]),
    install_requires=requirements,
    keywords="unsplash library",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    zip_safe=True,
)
