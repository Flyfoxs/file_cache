#!/usr/bin/env python
from setuptools import setup
import setuptools


with open('README.md') as file:
    long_description = file.read()

setup(
    name='file_cache',
    version='0.1.5',
    description='Cache dataframe with local hd5 file, and reduce the memory by convert type for number',
    long_description='File_cache can help you cache the pandas result with hd5 file, You can get demo from: https://github.com/Flyfoxs/file_cache/blob/master/demo.ipynb',
    url='https://github.com/Flyfoxs/file_cache',
    author='Felix Li',
    author_email='lilao@163.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='pandas file cache python file_cache',
    packages=setuptools.find_packages(),
)
