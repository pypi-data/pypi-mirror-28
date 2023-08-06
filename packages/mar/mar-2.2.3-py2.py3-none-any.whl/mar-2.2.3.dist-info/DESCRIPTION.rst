========
Overview
========



Package for handling Mozilla Archive files. MAR file format is documented at https://wiki.mozilla.org/Software_Update:MAR

* Free software: MPL 2.0 license

Usage
=====

To list the contents of a mar::

    mar -t complete.mar

To list the contents of a mar with extra detail::

    mar -T complete.mar

To extract a mar::

    mar -x complete.mar

To extract, and uncompress a bz2 compressed mar::

    mar -j -x complete.mar

To verify a mar::

    mar -k :mozilla-nightly -v complete.mar

To create a mar, using bz2 compression::

    mar -j -c complete.mar *

To create a mar, using xz compression::

    mar -J -c complete.mar *

To create a signed mar::

    mar -J -c complete.mar -k private.key -H nightly -V 123 tests

Installation
============

::

    pip install mar

Documentation
=============

https://mar.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox


Changelog
=========

2.2.3 (2018-01-18)
------------------
* Update dependencies; dependencies are now also pinned in setup.py
* Correct the key size in exception messages
* Fix for construct 2.8.22 and higher
* Fix for hypothesis 3.44.16

2.2.2 (2017-07-06)
-----------------------------------------
* Fix bug when writing MAR files: the index size was incorrect
* Support writing interable streams
* Add new Mozilla SHA384 public keys

2.2.1 (2017-08-23)
-----------------------------------------
* Output compression and signature type

2.1.0 (2017-06-28)
-----------------------------------------
* Implement XZ compression

2.0.0 (2017-01-12)
-----------------------------------------
* First release on PyPI.


