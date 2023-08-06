================================================
devpi-web: web interface plugin for devpi-server
================================================

This plugin adds a web interface with search for `devpi-server`_.

.. _devpi-server: http://pypi.python.org/pypi/devpi-server


Installation
============

``devpi-web`` needs to be installed alongside ``devpi-server``.

You can install it with::

    pip install devpi-web

There is no configuration needed as ``devpi-server`` will automatically discover the plugin through calling hooks using the setuptools entry points mechanism.


=========
Changelog
=========



.. towncrier release notes start

3.2.2 (2018-01-17)
==================

Bug Fixes
---------

- fix issue482: let external links in documentation open outside of iframe.

- Prevent stale static resources from browser caching by adding devpi-web
  version to their URLs.


3.2.1 (2017-11-23)
==================

No significant changes.


3.2.1rc1 (2017-09-08)
=====================

Bug Fixes
---------

- make search results compatible with pip showing INSTALLED/LATEST info.

- fix server error by returning 404 when a toxresult can't be found.


3.2.0 (2017-04-23)
==================

- version.pt: add "No releases" when there are none.

- project.pt: add "Documentation" column with link to documentation per version.


3.1.1 (2016-07-15)
==================

- removed unnecessary fetching of mirror data during indexing.



