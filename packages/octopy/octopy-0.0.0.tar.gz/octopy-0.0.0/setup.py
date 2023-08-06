from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='octopy',
    version='0.0.0',
    description='Github API',
    url='https://github.com/monzita/octopy',
    author='Monika Ilieva',
    author_email='monika.ilieva@protonmail.com',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6'
    ],

    keywords='github api octopy git client',
    packages=find_packages(exclude=['contrib', 'docs', 'tests', 'venv']),
)