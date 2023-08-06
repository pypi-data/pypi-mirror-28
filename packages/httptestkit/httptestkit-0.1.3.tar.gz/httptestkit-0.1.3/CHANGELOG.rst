==========
Change Log
==========

This document records all notable changes to httptestkit.

This project adheres to `Semantic Versioning <http://semver.org/>`_.

v0.1.3
======

Added:
******

* Plugin support to allow the easy addition of new features in a modular fashion.

Changed:
********

* Final sweep of all code to find every stupid webinspect name.
* Add long_description to setup.py.
* Rewrite dns lookup as a plugin.
* Rewrite ipinfo lookup as a plugin.
* Rewrite headers lookup as a plugin.

Removed:
********

* DNS lookups from inspector.
* IPInfo lookups from inspector.
* Header lookups from inspector.
* Helper methods from inspector.

v0.1.2
======

Added:
******

* None

Changed:
********

* Removed universal wheel requirement from setup.cfg (py3 only).
* More naming fixes (I have webinspect **everywhere**).

Removed:
********

* None

v0.1.1
======

Added:
*****

* None

Changed:
*******

* Bumped version number
* Fix references to the old name, webinspect, in AUTHORS, CHANGELOG, CONTRIBUTING

Removed:
********

* None
