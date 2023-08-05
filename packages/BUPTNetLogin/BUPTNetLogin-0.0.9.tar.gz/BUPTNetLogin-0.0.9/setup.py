# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

__author__ = 'ingbyr'

setuptools.setup(
    name='BUPTNetLogin',
    version='0.0.9',
    author='ingbyr',
    author_email='dev@ingbyr.com',
    url='http://www.ingbyr.com',
    description='Command line tool to login the BUPT net',
    packages=['BUPTLogin'],
    install_requires=[
         'beautifulsoup4',
        'lxml'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bnl = BUPTLogin.login:do_login',
            'bnlo = BUPTLogin.logout:logout'
        ]
    },
)
