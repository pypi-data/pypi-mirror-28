#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name     = 'cropper-img',
    version  = '0.1.4',
    packages = find_packages(),
    requires = ['python (>= 3.0)', 'Pillow (>=5.0)'],
    description  = 'image splitting',
    long_description = open('README.markdown').read(),
    author       = 'andry1983',
    author_email = 'andry1983g28@gmail.com',
    keywords     = 'images',
    classifiers  = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    zip_safe=False,
    entry_points="""
   [console_scripts]
   cropper-img = cropper_img.comix_img:start
   """
)