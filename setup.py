# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in publisher/__init__.py
from publisher import __version__ as version

setup(
	name='publisher',
	version=version,
	description='An app for handling publishing process',
	author='Alzad',
	author_email='a.moustafa@alzad.ae',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
