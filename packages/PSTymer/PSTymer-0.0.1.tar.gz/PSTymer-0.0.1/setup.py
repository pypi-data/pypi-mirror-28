#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from setuptools import setup, find_packages
 
setup(
    name='PSTymer',
    version="0.0.1",
    packages=find_packages(),
    author="Znax & reco team",
    description="Monitor time for Python code",
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved',
        'Programming Language :: Python :: 3.5',
	],
    include_package_data=True,
    url='https://github.com/Znax/python-simple-timer'
)