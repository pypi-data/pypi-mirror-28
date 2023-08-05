from distutils.core import setup
from setuptools import find_packages, setup, Command

setup(
  name = 'coinspot-py',
  packages = ['coinspot'], 
  version = '0.0.1',
  description = 'A python wrapper for the CoinSpot API',
  author = 'Slavko Bojanic',
  author_email = 'slavkobojj@gmail.com',
  url = 'https://github.com/slavkobojanic/Python-CoinSpot-V2', 
  download_url = 'https://github.com/slavkobojanic/Python-CoinSpot-V2/archive/0.0.1.tar.gz', # I'll explain this in a second
  keywords = ['python', 'coinspot', 'cryptocurrency', 'bitcoin', 'api', 'python3', 'altcoin'],
  classifiers = [],
  install_requires=[
        'requests'
    ],
  python_requires='>=3'
)