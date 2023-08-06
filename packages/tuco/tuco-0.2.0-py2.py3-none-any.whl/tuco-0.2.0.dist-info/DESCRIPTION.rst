========
Overview
========



A simple class based finite state machine with parsing time validation

* Free software: MIT license

Installation
============

::

    pip install tuco

Documentation
=============

https://python-tuco.readthedocs.io/

Development
===========
Make sure you have a running redis instance and to run the all tests run::

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

0.1.0
-----


