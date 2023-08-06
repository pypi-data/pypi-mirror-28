SciDB-Py: Python Interface to SciDB
===================================
.. image:: https://travis-ci.org/Paradigm4/SciDB-Py.svg
    :target: https://travis-ci.org/Paradigm4/SciDB-Py

Warning
-------

This is SciDB-Py Release **16.9.1**. This library has been released in
`September 2017` and has been rewritten entirely from scratch. This
version is **not compatible** with the previous versions of the
library. The documentation for the previous versions is available at
`SciDB-Py documentation (legacy)
<http://scidb-py.readthedocs.io/en/stable/>`_. GitHub pull requests
are still accepted for the previous versions, but the code is not
actively maintained.


Requirements
------------

SciDB ``16.9`` with Shim

Python ``2.7.x``, ``3.4.x``, ``3.5.x``, ``3.6.x`` or newer.

Required Python packages::

  backports.weakref
  enum34
  numpy
  pandas
  requests
  six


CentOS 6 and Red Hat Enterprise Linux 6
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CentOS ``6`` and Red Hat Enterprise Linux ``6`` come with Python
``2.6``. SciDB-Py requires Python ``2.7`` or newer (see above). The
default Python cannot be upgraded on these operating systems. Instead
a different Python version can be installed in parallel using
`Software Collections <https://www.softwarecollections.org/en/>`_. For
example, `here
<https://www.softwarecollections.org/en/scls/rhscl/python27/>`_ are
the instructions to install Python ``2.7`` using Software Collections.



Installation
------------

Install latest release::

  $ pip install scidb-py

Install development version from GitHub::

  $ pip install git+http://github.com/paradigm4/scidb-py.git


Documentation
-------------

See `SciDB-Py Documentation <http://paradigm4.github.io/SciDB-Py/>`_.


