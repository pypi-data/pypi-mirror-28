from distutils.core import setup
from setuptools import find_packages
setup(
  name = 'djcomp',
  # packages = ['djcomp'],
  packages = find_packages(exclude=['core','testapp','testapp.migrations']),
  version = '0.0.6',
  description = 'Django components',
  author = 'hieunv495',
  author_email = 'hieunv495@gmail.com',
  url = 'https://bitbucket.org/hieunv040995/djcomponents',
  download_url = 'https://bitbucket.org/hieunv040995/djcomponents/get/0.0.1.tar.gz',
  keywords = ['testing', 'logging', 'example'],
  classifiers = [])
