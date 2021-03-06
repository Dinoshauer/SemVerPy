from setuptools import setup
from semverpy import __version__, __author__, __license__


classifiers = [
    'Programming Language :: Python :: {}'.format(v)
    for v in (2, 2.7, 3, 3.3, 3.4, 3.5,)]


setup(
    name='SemVerPy',
    description='Bump versions. Semantically.',
    version=__version__,
    author=__author__,
    author_email='k@mackwerk.dk',
    license=__license__,
    url='https://github.com/Dinoshauer/SemVerPy',
    py_modules=['semverpy'],
    classifiers=classifiers
)
