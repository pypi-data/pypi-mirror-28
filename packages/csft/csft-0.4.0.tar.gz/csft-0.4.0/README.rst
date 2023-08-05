csft - Count Sizes of File Types
================================

.. image:: https://travis-ci.org/yanqd0/csft.svg?branch=master
   :target: https://travis-ci.org/yanqd0/csft
   :alt: Travis
.. image:: https://ci.appveyor.com/api/projects/status/hu856hh9u575t69t/branch/master?svg=true
   :target: https://ci.appveyor.com/project/yanqd0/csft/branch/master
   :alt: AppVeyor
.. image:: https://codecov.io/gh/yanqd0/csft/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/yanqd0/csft
   :alt: CodeCov
.. image:: https://requires.io/github/yanqd0/csft/requirements.svg?branch=master
   :target: https://requires.io/github/yanqd0/csft/requirements/?branch=master
   :alt: Requirements
.. image:: https://img.shields.io/github/license/yanqd0/csft.svg
   :target: https://github.com/yanqd0/csft/blob/master/LICENSE
   :alt: License

A CLI to count sizes of file types in a directory, implemented by Python.

Install
--------

.. image:: https://img.shields.io/pypi/v/csft.svg
   :target: https://pypi.python.org/pypi/csft
   :alt: PyPI
.. image:: https://img.shields.io/pypi/format/csft.svg
   :target: https://pypi.python.org/pypi/csft
   :alt: format
.. image:: https://img.shields.io/pypi/status/csft.svg
   :target: https://pypi.python.org/pypi/csft
   :alt: status
.. image:: https://img.shields.io/pypi/pyversions/csft.svg
   :target: https://pypi.python.org/pypi/csft
   :alt: versions

Install from the official PYPI::

    pip install csft

Install from the latest source::

    pip install git+https://github.com/yanqd0/csft.git

.. image:: https://img.shields.io/github/commits-since/yanqd0/csft/latest.svg
   :target: https://github.com/yanqd0/csft
   :alt: commits
.. image:: https://img.shields.io/github/issues/yanqd0/csft.svg
   :target: https://github.com/yanqd0/csft/issues
   :alt: issues

Usage
-----

The simplest usage::

    csft PATH/TO/A/DIRECTORY

More Usage::

    csft -h

CLI Results
-----------

Something like this::

    $ csft
            type       size
    0      .pack  116.11 MB
    1        .js   12.64 MB
    2      .json    6.68 MB
    3       .png    1.89 MB
    4      .html    1.57 MB
    5       .idx  974.77 KB
    6       .css  140.81 KB
    7              78.33 KB
    8      .gexf   51.33 KB
    9    .sample   15.32 KB
    10       .md   10.54 KB
    11  .LICENSE    1.06 KB
    12       .sh  292 bytes

Use as a Python module
----------------------

>>> from csft import csft2data
>>> data = csft2data('.')
>>> from pandas import DataFrame, Series
>>> isinstance(data, DataFrame)
True
>>> isinstance(data['size'], Series)
True
>>> isinstance(data['type'], Series)
True
