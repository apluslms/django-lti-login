#!/usr/bin/env python3
"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os.path import abspath, dirname, join

here = abspath(dirname(__file__))

# Get the long description from the README.rst file
with open(join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get requirements from the requirements.txt file
with open(join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = f.read()
requirements = [line.strip() for line in requirements.splitlines()]

setup(
    name='django-lti-login',
    version='3.3.0',
    description='A simple, yet powerful, LTI login application for Django.',
    long_description=long_description,
    keywords='django lti',
    url='https://github.com/apluslms/django-lti-login',
    author='Jaakko Kantojärvi',
    author_email='jaakko@n-1.fi',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',

        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=find_packages(exclude=['example']),
    include_package_data=True,
    install_requires=requirements,
)
