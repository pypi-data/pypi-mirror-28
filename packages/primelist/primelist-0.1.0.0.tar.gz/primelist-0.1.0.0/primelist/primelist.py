"""primelist
https://github.com/lapets/primelist

Python library encapsulating the set of all primes as a
an indexed collection (optimized for small primes).

"""

import doctest
from isqrt import isqrt

def _load():
    """Read prime entries from file system into list."""
    ps = []
    for digits in range(1,7):
        ps.extend(map(int, open("data/"+str(digits)).read().split("\n")))
    return ps


def _factor(ps, n):
    """Return first factor of n found in list of primes ps."""
    for p in ps:
        if p > isqrt(n):
            break
        if (n // p) * p == n:
            return p
    return None


def _next(ps):
    """Return the next prime given an exhaustive list of primes."""
    if len(ps) == 0:
        return 2
    if len(ps) == 1:
        return 3
    n = ps[-1] + 2
    while True:
        if _factor(ps, n) is None:
            return n
        n += 2


def _getitem(ps, key):
    """Return the next prime given an exhaustive list of primes."""
    if isinstance(key, slice):
        if key.step is not None and key.step != 1:
            raise ValueError("Only an increment of 1 is supported.")
        index_bound = max(key.start, key.stop)
    elif type(key) is int:
        if key < 0:
            raise ValueError("Supplied index is negative.")
        index_bound = key

    while len(ps) <= index_bound:
        ps.append(_next(ps))
    return ps[key]


def _contains(ps, n):
    """Test whether n is a prime number."""
    if n > ps[-1] and _factor(ps, n) is not None:
        return False
    while ps[-1] < n:
        ps.append(_next(ps))
    return ps[-1] == n or n in ps


class _meta(type):
    """
    Metaclass to provide static methods.

    >>> 17 in primelist
    True
    >>> 14 in primelist
    False
    >>> 1000000000000000000000000000 in primelist
    False
    >>> 1000003 in primelist
    True
    >>> 1000004 in primelist
    False
    >>> primelist[0]
    2
    >>> primelist[79905]
    1019173
    >>> primelist[1:6]
    [3, 5, 7, 11, 13]
    """
    def __getitem__(self, key):
        return _getitem(_load(), key)

    def __contains__(self, n):
        return _contains(_load(), n)

    def __len__(self):
        raise ArithmeticError("There are infinitely many primes.")


class primelist(object, metaclass=_meta):
    """
    Class encapsulating the sequence of all primes.

    >>> ps = primelist()
    >>> 17 in ps
    True
    >>> 14 in ps
    False
    >>> 1000000000000000000000000000 in ps
    False
    >>> 1000003 in ps
    True
    >>> 1000004 in ps
    False
    >>> ps[0]
    2
    >>> ps[79905]
    1019173
    >>> ps[1:6]
    [3, 5, 7, 11, 13]
    >>> l = len(ps)
    >>> p = ps[79906]
    >>> len(ps) >= l
    True
    """
    def __init__(self):
        self.entries = _load()

    def __getitem__(self, key):
        return _getitem(self.entries, key)

    def __contains__(self, n):
        return _contains(self.entries, n)

    def __len__(self):
        """Number of prime entries already computed and stored."""
        return len(self.entries)


if __name__ == "__main__": 
    doctest.testmod()
