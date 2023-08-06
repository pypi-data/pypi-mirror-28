#setup.py
"""  """

from setuptools import setup, find_packages
from codecs import open
from os import path

#here = path.abspath(path.dirname(__file__))

#with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#    long_description = f.read()


setup(
       name          = 'botsallytest',
       version       = '1.2.1',
       py_modules    = ['botsallytest'],
       author        = 'botsally',
       author_email  = 'bot@botsally.com',
       url           = 'https://www.botsally.com',
       description   = 'A test home work of botsally',
       packages      = find_packages(exclude=['contrib', 'docs', 'tests']),

     )

