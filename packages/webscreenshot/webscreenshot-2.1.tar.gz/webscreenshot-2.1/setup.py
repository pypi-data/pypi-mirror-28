#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='webscreenshot',
      version='2.1',
      description='A simple script to screenshot a list of websites',
      long_description=open('webscreenshot/README.md').read(),
      url='https://github.com/maaaaz/webscreenshot',
      author='Thomas D.',
      author_email='tdebize@mail.com',
      license='LGPL',
      classifiers=[
        'Topic :: Security',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
      ],
      keywords='webscreenshot web screenshot phantomjs',
      packages=find_packages(),
      python_requires='<3',
      entry_points = {
        'console_scripts': ['webscreenshot=webscreenshot.webscreenshot:main'],
      },
      include_package_data=True)