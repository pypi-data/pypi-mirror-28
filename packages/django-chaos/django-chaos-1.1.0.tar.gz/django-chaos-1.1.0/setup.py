#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    """Retrieves the version from chaos/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = '1.1.0'


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-chaos',
    version=version,
    description="""Chaos is a project that you can use to do project management""",
    long_description=readme + '\n\n' + history,
    author='George Silva',
    author_email='george@sigmageosistemas.com.br',
    url='https://gitlab.sigmageosistemas.com.br/dev/django-chaos',
    packages=[
        'chaos',
    ],
    include_package_data=True,
    install_requires=[
        'django',
        'django-file-context',
        'django-common-models',
        'django-colorfield',
        'django-mptt',
        'django-taggit',
        'django-taggit-serializer',
        'django-dirtyfields',
        'django-filter',
        'django-recurrence',
        'jsonfield',
        'djangorestframework',
        'djangorestframework-filters',
        'icalendar',
        'pyexcel',
        'pyexcel-io',
        'pyexcel-xlsx',
        'django-excel',
        'pyexcel-webio',
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-chaos',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
