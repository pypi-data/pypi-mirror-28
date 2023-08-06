#!/usr/bin/env python

# Project skeleton maintained at https://github.com/jaraco/skeleton

import io

import setuptools

with io.open('README.rst', encoding='utf-8') as readme:
	long_description = readme.read()

name = 'pmxbot.saysomething'
description = 'Markov chain phrase generator for pmxbot'
nspkg_technique = 'managed'
"""
Does this package use "native" namespace packages or
pkg_resources "managed" namespace packages?
"""

params = dict(
	name=name,
	use_scm_version=True,
	author="Jason R. Coombs",
	author_email="jaraco@jaraco.com",
	description=description or name,
	long_description=long_description,
	url="https://github.com/yougov/" + name,
	packages=setuptools.find_packages(),
	include_package_data=True,
	namespace_packages=(
		name.split('.')[:-1] if nspkg_technique == 'managed'
		else []
	),
	python_requires='>=3.4',
	install_requires=[
		'more_itertools',
		'jaraco.collections',
		'jaraco.mongodb',
	],
	extras_require={
		'testing': [
			'pytest>=2.8',
			'pytest-sugar',
			'collective.checkdocs',
			'pmxbot>=1121',
		],
		'docs': [
			'sphinx',
			'jaraco.packaging>=3.2',
			'rst.linker>=1.9',
		],
	},
	setup_requires=[
		'setuptools_scm>=1.15.0',
	],
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: MIT License",
		"Programming Language :: Python :: 3",
	],
	entry_points={
		'pmxbot_handlers': [
			'pmxbot say something = pmxbot.saysomething:Chains.initialize',
		],
	},
)
if __name__ == '__main__':
	setuptools.setup(**params)
