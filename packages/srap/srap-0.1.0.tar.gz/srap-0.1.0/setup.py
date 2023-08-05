#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement

import sys
if sys.version_info < (2, 5):
    sys.exit('Python 2.5 or greater is required.')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import srap

with open('LICENSE') as fp:
    license = fp.read()

setup(name = 'srap',
      version = srap.__version__,
      description = 'Simple reflect annotation protocol lib.',
      long_description = '',
      author = 'Zhiwei Ao',
      author_email = '164439244@qq.com',
      maintainer = 'Zhiwei Ao',
      maintainer_email = '164439244@qq.com',
      url = 'https://github.com/aozhiwei/srap',
      packages = ['srap'],
      license = license,
      platforms = ['any'],
      classifiers = []
      )
