#!/usr/bin/env python
from setuptools import setup
from io import open

def readme():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()

setup(name='ListBot',
      version='1.0.1.2',
      description='Python Telegram bot',
      long_description=readme(),
      author='vladislavburch',
      author_email='vladislavburch17@gmail.com',
      url='https://github.com/vladislavburch/ListBot',
      packages=['ListBot'],
      license='GPL2',
      keywords='telegram bot',
      install_requires=['requests', 'six'],
      extras_require={
          'json': 'ujson',
      },
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 3',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ]
      )
