#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')
version = open('VERSION').read().strip()

setup(
    name='django-north',
    version=version,
    description="""Yet another way to manage migrations: DBA as a service""",
    long_description=readme + '\n\n' + history,
    author=u'Lauréline Guérin',
    author_email='laureline.guerin@people-doc.com',
    url='https://github.com/peopledoc/django-north',
    packages=[
        'django_north',
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.8,<2.0",
        "sqlparse",
        "six",
    ],
    tests_require=["tox"],
    license="MIT",
    zip_safe=False,
    keywords='django-north',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
