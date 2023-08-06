# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

# $ python setup.py test -s tests.PackagesTests.test_packages

SETUP_INFO = dict(
    name='lino-amici',
    version='18.1.0',
    install_requires=['lino-xl', 'vobject'],

    # tests_require=['pytest', 'mock'],
    test_suite='tests',
    description=("A Lino application for managing family contacts"),
    long_description="""\
.. image:: https://readthedocs.org/projects/lino/badge/?version=latest
    :alt: Documentation Status
    :target: http://lino.readthedocs.io/en/latest/?badge=latest

.. image:: https://coveralls.io/repos/github/lino-framework/noi/badge.svg?branch=master
    :target: https://coveralls.io/github/lino-framework/noi?branch=master

.. image:: https://travis-ci.org/lino-framework/noi.svg?branch=stable
    :target: https://travis-ci.org/lino-framework/noi?branch=stable

.. image:: https://img.shields.io/pypi/v/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

.. image:: https://img.shields.io/pypi/l/lino-noi.svg
    :target: https://pypi.python.org/pypi/lino-noi/

Lino Amici is a customizable Lino application for managing family
contacts.  It is currently a submarine project, used only by its
author and therefore poorly documented.

- The central project homepage is http://amici.lino-framework.org

- For *introductions* and *commercial information* about Lino Amici
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net>`__.


""",
    author='Luc Saffre',
    author_email='luc@lino-framework.org',
    url="http://amici.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 4 - Beta
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
Intended Audience :: Information Technology
Intended Audience :: Customer Service
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Software Development :: Bug Tracking
Topic :: Communications :: Email :: Address Book
Topic :: Office/Business :: Groupware
""".splitlines())

SETUP_INFO.update(packages=[str(n) for n in """
lino_amici
lino_amici.lib
lino_amici.lib.amici
lino_amici.lib.amici.fixtures
lino_amici.lib.contacts
lino_amici.lib.contacts.fixtures
lino_amici.projects
lino_amici.projects.herman
lino_amici.projects.herman.settings
lino_amici.projects.herman.settings.fixtures
lino_amici.projects.herman.tests
""".splitlines() if n])

SETUP_INFO.update(message_extractors={
    'lino_amici': [
        ('**/cache/**',          'ignore', None),
        ('**.py',                'python', None),
        ('**.js',                'javascript', None),
        ('**/config/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(include_package_data=True, zip_safe=False)
# SETUP_INFO.update(package_data=dict())


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l

# l = add_package_data('lino_noi.lib.noi')
# for lng in 'de fr'.split():
#     l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
