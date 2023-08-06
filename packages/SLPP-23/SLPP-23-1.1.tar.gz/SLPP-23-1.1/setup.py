#!/usr/bin/env python
from setuptools import setup

setup(
    name='SLPP-23',
    description='SLPP-23 is a simple lua-python data structures parser',
    version='1.1',
    author='Ilya Skriblovsky',
    author_email='ilyaskriblovsky@gmail.com',
    url='https://github.com/IlyaSkriblovsky/slpp-23',
    license='https://github.com/IlyaSkriblovsky/slpp-23/blob/master/LICENSE',
    keywords=['lua'],
    py_modules=['slpp'],
    install_requires=['six'],
)
