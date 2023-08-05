from setuptools import setup, find_packages
import os.path

setup(
	name='pygrt',
	version='1.0.0',
	packages=find_packages(),
	description='Thin API wrapper for GRT Realtime API',
	author="Harley Benoit (@s0i)",
	install_requires=['requests']
)