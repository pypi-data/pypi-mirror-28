#!/usr/bin/env python3
# encoding: utf-8
from distutils.core import setup, Extension

strextnd_module = Extension('strextnd', sources = ['strextnd.c'])

setup(name='strextnd',
      version='0.3',
      description='A Module written in C that extends the python3 str library',
      author = 'Ariel Ferdman',
      author_email = 'arielxcon@gmail.com',
      ext_modules=[strextnd_module],
      url = 'https://github.com/arielferdman/strextnd',
      download_url = 'https://github.com/arielferdman/strextnd/archive/0.3.tar.gz',
      keywords = ['string', 'is_numeric', 'float'],
      classifiers = [],)
