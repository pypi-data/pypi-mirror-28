#!/usr/bin/env python
# coding=utf-8

import codecs
from setuptools import setup, find_packages

setup(
    name='x-py',
    version='0.0.1',
    description=u'x-py',
    long_description= codecs.open('README.rst','r+','utf-8').read(),
    author='yoshow',
    author_email='ruanyu@live.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=[],
    platforms=["all"],
    url='https://github.com/yoshow/x-py'
    # entry_points={
    #    'console_scripts': [
    #        'x=x_pill:x',
    #        'pill=x_pill:pill'
    #    ]
    # }
)
