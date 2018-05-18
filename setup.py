#!/usr/bin/env python3
"""CampsiteFinder: Web scraper to pick up last minute campsites.

TODO: longer description -- this portion will go into 'long_description'
in the setup metadata.
"""

from __future__ import print_function
from setuptools import setup


DOCLINES = (__doc__ or '').split('\n')

CLASSIFIERS = """\
Intended Audience :: Recreation
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Topic :: Recreation
Operating System :: Unix
Operating System :: MacOS
"""

MAJOR               = 1
MINOR               = 0
MICRO               = 0
VERSION             = '{}.{}.{}'.format(MAJOR, MINOR, MICRO)


# TODO: maintainer
# TODO: maintainer_email
# TODO: author
# TODO: license

setup(
    name = 'campsiteFinder',
    description = DOCLINES[0],
    long_description = '\n'.join(DOCLINES[2:]),
    #url = 'https://github.com/anp-lbl/becquerel/wiki',
    download_url = 'https://github.com/wjvanderlip/Vanderlip_AY250_HW/tree/master/final_project',
    classifiers=[_f for _f in CLASSIFIERS.split('\n') if _f],
    platforms = ['Linux',  'Mac OS-X', 'Unix'],
    packages=[
        'campsiteFinder',
        #'becquerel.core',
        #'becquerel.parsers',
        #'becquerel.tools',
    ],
    #setup_requires=[],
    tests_require=['unittest'],
    package_data={'campsiteFinder': ['*.csv']}
)
