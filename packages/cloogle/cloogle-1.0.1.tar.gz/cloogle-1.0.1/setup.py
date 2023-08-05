"""The setuptools based setup module for cloogle."""

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cloogle',
    version='1.0.1',
    description='Basic interface to the Cloogle API',
    long_description=long_description,
    url='https://github.com/clean-cloogle/cloogle',
    author='Camil Staps',
    author_email='info@camilstaps.nl',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities',
    ],
    keywords='cloogle api search clean',
    py_modules=['cloogle']
)
