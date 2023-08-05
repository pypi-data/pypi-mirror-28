#!/usr/bin/env python
# coding=utf-8
from setuptools import setup




setup(
    name='pandas-files',
    version='0.2.3',
    author='GraySilver',
    author_email='allenyzx@163.com',
    url='https://upload.pypi.org/allenyzx/',
    description='This is a micro-distributed storage service.',
    packages=['pandasfiles','pandasfiles/base','pandasfiles/utils',
              'pandasfiles/tmp','pandasfiles/log','pandasfiles/conf'],
    install_requires=[
        "pandas>=0.18.1",
        "joblib>=0.11",
    ],
    license='MIT',
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.5",
    ],
)