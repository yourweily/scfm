try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'structured cashflow model',
    'author': 'Wei Li',
    'author_email': 'weily.li@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['view', 'util', 'po', 'controller'],
    'scripts': [],
    'name': 'scfm'
}

setup(**config)