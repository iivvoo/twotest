from setuptools import setup, find_packages
import os

version = '0.9.2'

setup(name='twotest',
      version=version,
      description="It takes Two to Django. py.test support for Django",
      long_description=open("README.txt").read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Ivo van der Wijk',
      author_email='two@in.m3r.nl',
      url='http://github.com/iivvoo/two.test',
      license='BSD',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytest',
      ],
      entry_points={
      },

      )

