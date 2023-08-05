#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='nmaptocsv',
      version='1.2',
      description='A simple python script to convert Nmap output to CSV',
      long_description=open('nmaptocsv/README.md').read(),
      url='https://github.com/maaaaz/nmaptocsv',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='LGPL',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      ],
      keywords='nmap scan output csv',
      packages=find_packages(),
      python_requires='<3',
      entry_points = {
        'console_scripts': ['nmaptocsv=nmaptocsv.nmaptocsv:main'],
      },
      include_package_data=True)