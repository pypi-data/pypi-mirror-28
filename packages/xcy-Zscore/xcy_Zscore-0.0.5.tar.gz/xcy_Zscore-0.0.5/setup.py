#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='xcy_Zscore',
    version='0.0.5',
    author='ChuanyuXue',
    author_email='cs_xcy@126.com',
    url='https://github.com/ChuanyuXue/mysmod/blob/master/zscore.py',
    description=u'A small tool of Zscore based on numpy',
    packages=['xcy_Zscore'],
    install_requires=["numpy >= 1.0.0"],
)