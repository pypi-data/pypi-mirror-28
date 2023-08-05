#!/usr/bin/env python

import os
import re
try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError("Could not import \"setuptools\"."
                      "Please install the setuptools package.")


def text_of(relpath):
    """
    Return string containing the contents of the file at *relpath* relative to
    this file.
    """
    thisdir = os.path.dirname(__file__)
    file_path = os.path.join(thisdir, os.path.normpath(relpath))
    with open(file_path) as f:
        text = f.read()
    return text


# Read the version without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = re.search(
    "__version__ = '([^']+)'", text_of('jsonrepo/__init__.py')
).group(1)


NAME = 'python-jsonrepo'
VERSION = version
DESCRIPTION = 'A simple repository for json serializable objects'
KEYWORDS = 'json repository'
AUTHOR = 'Romary Dupuis'
AUTHOR_EMAIL = 'romary@me.com'
URL = 'https://github.com/romaryd/python-jsonrepo'
LICENSE = text_of('LICENSE')
PACKAGES = find_packages(exclude=['tests', 'tests.*'])

INSTALL_REQUIRES = ['python-awesome-decorators',
                    'python-logging-mixin',
                    'python-singleton',
                    'six',
                    'redis',
                    'boto3']
TEST_SUITE = 'tests'
TESTS_REQUIRE = ['pytest']

CLASSIFIERS = [
    'Development Status :: 1 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities',
]

LONG_DESCRIPTION = text_of('README.md')


params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          LICENSE,
    'packages':         PACKAGES,
    'install_requires': INSTALL_REQUIRES,
    'tests_require':    TESTS_REQUIRE,
    'test_suite':       TEST_SUITE,
    'classifiers':      CLASSIFIERS,
}

if __name__ == '__main__':
    setup(**params)
