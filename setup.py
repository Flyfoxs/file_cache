#!/usr/bin/env python
from setuptools import setup
import setuptools

setup(
    name='file_cache',
    version='0.1.1.3',
    description='Cache dataframe with local file',
    url='https://github.com/Flyfoxs/file_cache',
    author='Felix Li',
    author_email='lilao@163.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='pandas cache python',
    packages=setuptools.find_packages(),
)
