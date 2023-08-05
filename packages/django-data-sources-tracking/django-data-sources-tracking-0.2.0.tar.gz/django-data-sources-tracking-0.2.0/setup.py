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
    """Retrieves the version from data_sources_tracking/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("data_sources_tracking", "__init__.py")


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
    name='django-data-sources-tracking',
    version=version,
    description="""Django app for dealing with files/data sources and tracking them. Useful for tracking public annotations or bfx pipeline outputs""",
    long_description=readme + '\n\n' + history,
    author='Michael A. Gonzalez',
    author_email='genomics.geek.04.22@gmail.com',
    url='https://github.com/genomics-geek/django-data-sources-tracking',
    packages=[
        'data_sources_tracking',
    ],
    include_package_data=True,
    install_requires=[
        'djangorestframework==3.7.7',
        'django-filter==1.1.0',
        'django-genomix==0.3.0',
        'django-model-utils==3.0.0',
        'django-user-activities==0.2.0',
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-data-sources-tracking',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
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
