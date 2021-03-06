#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.version_info < (3, 5, 0):
    raise RuntimeError("aiogrn requires Python 3.5+")

exec(open('aiogrn/_version.py').read())

setup(
    name='aiogrn',
    version=__version__,
    description="asyncio Groonga Client library",
    long_description=open("README.rst").read(),
    license='MIT License',
    author='Hideo Hattori',
    author_email='hhatto.jp@gmail.com',
    url='https://github.com/hhatto/aiogrn',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    install_requires=['aiohttp', 'async_timeout', 'poyonga'],
    keywords="asyncio groonga http gqtp",
    packages=['aiogrn'],
    zip_safe=False,
)
