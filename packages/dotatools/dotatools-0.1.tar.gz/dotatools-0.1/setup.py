#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup

setup(name="dotatools",
	version="0.1",
	description="OpenDota API wrapper",
	long_description="dotatools is an API wrapper for the open API supplied by OpenDota",
	url="http://github.com/marcusmunch/dotatools",
	license="GPLv3",
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		"Natural Language :: English",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6"
	],
	author="Marcus Grünewald",
	author_email="marcus@marcusmunch.dk",
	packages=["dotatools"],
	install_requires=["requests"]
	)
