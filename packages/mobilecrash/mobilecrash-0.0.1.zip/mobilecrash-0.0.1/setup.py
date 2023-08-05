# -*- coding:UTF-8 -*-
from __future__ import unicode_literals

from setuptools import setup, find_packages

setup(
    name= 'mobilecrash',
    version= '0.0.1',
    keywords= ('crash'),
    description= 'crash log collection',
    license= 'MIT License',
    install_requires = ['Django>=1.8', 'djangorestframework>=3.1.0'],

    author= 'ck',
    author_email= 'ck@all.com',

    packages = find_packages(),
    platforms= 'any',
)