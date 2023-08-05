from distutils.core import setup

setup(
  name = 'sense-energy',
  packages = ['sense-energy'], 
  install_requires=[
      'requests',
      'websocket-client',
  ],
  version = '0.1',
  description = 'API for the Sense Energy Monitor',
  author = 'scottbonline',
  author_email = 'scottbonline@gmail.com',
  url = 'https://github.com/scottbonline/sense',
  download_url = 'https://github.com/scottbonline/sense/archive/0.1.tar.gz', 
  keywords = ['sense', 'energy', 'api'], 
  classifiers = [],
)
