from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'mylibjay1',
    version = '0.0.1',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'MIT License',
	py_modules=['mylibllx'],

    author = 'ljx',
    author_email = '261958374@qq.com',

    packages = find_packages(),
    platforms = 'any',
)