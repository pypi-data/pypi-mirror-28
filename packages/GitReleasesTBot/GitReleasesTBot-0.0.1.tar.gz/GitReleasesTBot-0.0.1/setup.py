##
## Copyright (c) 2018 Nelly Simkova.
##
## This file is part of GitReleasesTBot
## (see https://github.com/sk8higher/GitReleasesTBot).
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program. If not, see <http://www.gnu.org/licenses/>.
##
import sys
from setuptools import setup, find_packages

requires = [
    'pytelegrambotapi',
]

setup(
    name='GitReleasesTBot',
    version='0.0.1',
    description=' ',
    url='https://github.com/sk8higher/GitReleasesTBot',
    download_url='https://github.com/sk8higher/GitReleasesTBot/archive/0.0.1.tar.gz',
    author='Nelly Simkova',
    author_email='sk8higher@iballwasrawt.ru',
    license='GPL-3.0',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires = requires,
    entry_points={
        'console_scripts': [
            'GitReleasesTBot=GitReleasesTBot.app:main',
        ],
    },
    test_suite='nose.collector',
    keywords=['github', 'git', 'release', 'telegram', 'bot']
)
