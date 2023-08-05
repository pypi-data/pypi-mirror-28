pytest-tap is a reporting plugin for pytest that outputs
`Test Anything Protocol (TAP) <http://testanything.org/>`_ data.
TAP is a line based test protocol for recording test data in a standard way.

Follow development on `GitHub <https://github.com/python-tap/pytest-tap>`_.
Developer documentation is on
`Read the Docs <https://tappy.readthedocs.io/>`_.


Releases
========

Version 2.2, January 9, 2018
----------------------------

* Update output format to match closer to pytest styling.
* Drop support for Python 3.3 (it is end-of-life).

Version 2.1, August 12, 2017
----------------------------

* Add support for Python 3.6.
* Fix crash when running with pytest-xdist (#27).

Version 2.0, August 1, 2016
---------------------------

* Update to tap.py 2.0.
  This update drops the indirect dependencies on nose and pygments.
* Improve handling of skips and xfails.
* Suppress ``# TAP results for TestCase`` for streaming.
  This header makes little sense for pytest's test function paradigm.
  Including the header generated extra noise for each function.
* Drop support for Python 2.6

Version 1.9, Released June 11, 2016
-----------------------------------

* Initial release as stand-alone plugin.
  The version number aligns with tappy.


