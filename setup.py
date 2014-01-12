#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
	name='jutsu',
	version='1.0',
	url='http://github.com/spektom/jutsu/',
	license='Apache 2.0',
	author='Michael Spector',
	author_email='spektom@gmail.com',
	long_description=__doc__,
	packages=find_packages(),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		'Flask',
		'Flask-SqlAlchemy',
		'apt_pkg'
	]
)
