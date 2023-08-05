#!/usr/bin/python

from setuptools import setup

setup(
    name='django-denorm',
    version='1.0.0dev',
    description='Denormalization magic for Django',
    long_description='django-denorm is a Django application to provide automatic management of denormalized database fields.',
    author=', '.join((
        'Christian Schilling <initcrash@gmail.com>',
        'James Turnbull <james@incuna.com>',
        'Petr Dlouhy <petr.dlouhy@email.cz>',
    )),
    author_email='django-denorm@googlegroups.com',
    url='http://github.com/django-denorm/django-denorm/',
    download_url='http://github.com/django-denorm/django-denorm/downloads',
    install_requires=[
        'six',
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    packages=[
        'denorm',
        'denorm.db',
        'denorm.db.mysql',
        'denorm.db.postgresql',
        'denorm.db.sqlite3',
        'denorm.management',
        'denorm.management.commands',
        'denorm.migrations',
    ],
)
