#!/usr/bin/env python
# vim: set fileencoding=utf-8 nofoldenable:

from setuptools import setup


VERSION = "1.0"

classifiers = [
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Natural Language :: English',
    'Operating System :: Unix',
    'Programming Language :: Python',
    ]

PACKAGE_DATA = {
    "sayhours": ["sounds/%02u/*.ogg" % h for h in range(24)],
}

LONG_DESC = """Speaks current time aloud."""


setup(
    name = 'sayhours',
    version = VERSION,
    author = 'Justin Forest',
    author_email = 'hex@umonkey.net',
    url = 'https://umonkey.net/',

    packages = ['sayhours'],
    package_dir = {'sayhours': 'sayhours'},
    package_data = PACKAGE_DATA,
    scripts = ['bin/sayhours'],

    classifiers = classifiers,
    description = 'Speaks current time aloud.',
    long_description = LONG_DESC,
    license = 'GNU GPL',
)
