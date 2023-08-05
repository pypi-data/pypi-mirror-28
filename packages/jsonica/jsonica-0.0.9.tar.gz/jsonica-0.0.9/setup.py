#!/usr/bin/env python3
# coding:utf-8

from setuptools import setup, find_packages

setup(name='jsonica',
      version='0.0.9',
      description='manage huge json as xlsx statistically.',
      author='setminami',
      author_email='set.minami@gmail.com',
      url='https://setminami.github.io/Jsonica/',
      packages=find_packages(exclude=['contrib', 'docs', 'output', 'Samples', 'tests']),
      install_requires=['openpyxl>=2.4.9', 'PyYAML>=3.12', 'jsonschema>=2.6.0'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
    )
