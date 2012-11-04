#!/usr/bin/env python
# coding: utf-8

import os
from distutils.core import setup

version = '0.0.1'

root_dir = os.path.dirname(__file__)
if not root_dir:
    root_dir = '.'

long_desc = open(os.path.join(root_dir, 'README.md')).read()

setup(
    name='sorl-defined-thumbnail',
    version=version,
    url='https://github.com/jjdelc/sorl-defined-thumbnails',
    download_url='https://github.com/jjdelc/sorl-defined-thumbnails/archive/master.zip',
    author=u'Jesús Del Carpio',
    author_email='jjdelc@gmail.com',
    license='BSD License',
    py_modules=['defined_thumbnails'],
    packages=['defined_thumbnails', 'defined_thumbnails.templatetags'],
    description='A sorl-thumbnail extension to restrict the thumbnail'
        'generation to a pre defined set of values',
    long_description=long_desc,
)
