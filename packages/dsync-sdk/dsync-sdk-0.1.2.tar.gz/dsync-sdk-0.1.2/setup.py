# -*- coding: utf-8 -*-
"""
This file is part of the DSYNC Python SDK package.

(c) DSYNC <support@dsync.com>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""
# Learn more: https://github.com/dsync-dev/python-sdk

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='dsync-sdk',
    version='0.1.2',
    description='Python SDK for realtime synchronization with DSYNC',
    long_description=readme,
    author='DSYNC',
    author_email='support@dsync.com',
    url='https://github.com/dsync-dev/python-sdk',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='dsync, sdk, api',
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
)

