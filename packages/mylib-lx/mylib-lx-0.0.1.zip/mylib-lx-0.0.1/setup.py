from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'mylib-lx',
    version = '0.0.1',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'MIT License',

    author = 'jim',
    author_email = '261958374@qq.com',

    packages = find_packages(),
    platforms = 'any',
)