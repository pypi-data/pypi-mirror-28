=========
primelist
=========

Python library encapsulating the set of all primes as an indexed collection (optimized for small primes).

.. image:: https://badge.fury.io/py/primelist.svg
   :target: https://badge.fury.io/py/primelist
   :alt: PyPI version and link.

Purpose
-------
Native Python class that encapsulates the set of all primes as an ascending sequence. Optimizations are included for finding and generating relatively small prime numbers.

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install primelist

The library can be imported in the usual way::

    from primelist import primelist

Examples
--------
The library provides a static class that behaves like a list-like object that virtually contains all prime numbers::

    >>> 17 in primelist
    True
    >>> 1000000000000000000000000000 in primelist
    False
    >>> primelist[0]
    2
    >>> primelist[79905]
    1019173
    >>> primelist[1:6]
    [3, 5, 7, 11, 13]

All prime numbers up to six digits in length are loaded into memory from disk on every one of the above queries. If an expression requires a larger range of primes to succeed, additional primes are generated as necessary in ascending order (inefficiently).

To maintain the list of primes in memory (both those loaded and those subsequently generated due to additional method invocations), it is possible to instead create an object. The object's methods are the same as those of the class `primelist`::

    >>> ps = primelist()
    >>> 17 in ps
    True
    >>> 1000000000000000000000000000 in ps
    False
    >>> ps[0]
    2
    >>> ps[79905]
    1019173
    >>> ps[1:6]
    [3, 5, 7, 11, 13]

It is possible to use the `len` function to obtain the number of primes that have been computed and stored so far within the object. The output below may not match exactly what you see in your environment::

    >>> ps = primelist()
    >>> len(ps)
    78498
