================================
python-anyconfig-bson-backend
================================

.. image:: https://img.shields.io/pypi/v/anyconfig-bson-backend.svg
   :target: https://pypi.python.org/pypi/anyconfig-bson-backend/
   :alt: [Latest Versbson]

.. image:: https://img.shields.io/travis/ssato/python-anyconfig-bson-backend.svg
   :target: https://travis-ci.org/ssato/python-anyconfig-bson-backend
   :alt: Test status

.. image:: https://img.shields.io/coveralls/ssato/python-anyconfig-bson-backend.svg
   :target: https://coveralls.io/r/ssato/python-anyconfig-bson-backend
   :alt: Coverage Status

.. image:: https://landscape.io/github/ssato/python-anyconfig-bson-backend/master/landscape.png
   :target: https://landscape.io/github/ssato/python-anyconfig-bson-backend/master
   :alt: Code Health

This is a backend module for python-anyconfig to load and dump BSON files w/
using pymongo, https://pypi.python.org/pypi/pymongo/ [#]_ .

- Author: Satoru SATOH <ssato@redhat.com>
- License: MIT

SEE ALSO:

- python-anyconfig: https://pypi.python.org/pypi/anyconfig
- pymongo: https://pypi.python.org/pypi/pymongo/
- BSON spec: http://bsonspec.org/

- Download:

  - PyPI: https://pypi.python.org/pypi/anyconfig-bson-backend
  - Copr RPM repos: https://copr.fedoraproject.org/coprs/ssato/python-anyconfig/

.. [#] bson from pymongo package may work and bson, https://pypi.python.org/pypi/bson/, does not.

Build & Install
================

If you're Fedora or Red Hat Enterprise Linux user, try::

  $ python setup.py srpm && mock dist/<package>-<ver_dist>.src.rpm
  
or::

  $ python setup.py rpm

and install built RPMs.

Otherwise, try usual ways to build and/or install python modules such like
'python setup.py bdist', etc.

.. vim:sw=2:ts=2:et:
