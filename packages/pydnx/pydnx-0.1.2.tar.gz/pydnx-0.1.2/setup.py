try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION="0.1.2"

config = {
    'description': 'pydnx',
    'author': 'Sean Mosely',
    'author_email': 'sean.mosely@gmail.com',
    'version': VERSION,
    'install_requires': ['lxml>=3.6.4',],
    'packages': ['pydnx'],
    'scripts': [],
    'description': 'Package for generating DNX XML for the Ex Libris Rosetta digital preservation application',
    'name': 'pydnx',
    'download_url': 'https://github.com/NLNZDigitalPreservation/pydnx/archive/v'+VERSION+'.tar.gz',
    'license': 'MIT',
}

setup(**config)
