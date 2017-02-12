import re
import os
import codecs

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def find_version(*parts):
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(here, *parts), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*parts):
    with codecs.open(os.path.join(here, *parts), encoding='utf-8') as f:
        return f.read()


setup(
    name = 'pickle-peeker',
    version = find_version('ppk', '__init__.py'),
    # url = '',
    license = 'MIT',
    author = 'Paolo Dragone',
    author_email = 'dragone.paolo@gmail.com',
    description = 'A smart pickle reader.',
    #long_description = read('README.rst'),
    packages = find_packages(exclude=['*tests*']),
    # test_suite = '',
    platforms = 'any',
    classifiers = [
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points = {
        'console_scripts': [
            'ppk=ppk:main'
        ]
    }
)
