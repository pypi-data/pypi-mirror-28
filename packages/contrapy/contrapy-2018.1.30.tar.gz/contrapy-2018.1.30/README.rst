contrapy
========

Contracts for Python 3

.. image:: https://snyk.io/test/github/digitalmensch/contrapy/badge.svg
   :target: https://snyk.io/test/github/digitalmensch/contrapy

.. image:: https://travis-ci.org/digitalmensch/contrapy.svg?branch=master
    :target: https://travis-ci.org/digitalmensch/contrapy

.. image:: https://coveralls.io/repos/github/digitalmensch/contrapy/badge.svg?branch=master
   :target: https://coveralls.io/github/digitalmensch/contrapy?branch=master

.. image:: https://img.shields.io/pypi/pyversions/contrapy.svg
   :target: https://pypi.python.org/pypi/contrapy

.. image:: https://img.shields.io/pypi/l/contrapy.svg
   :target: https://github.com/digitalmensch/contrapy/blob/master/LICENSE

Examples
--------

.. code:: python

    import contrapy
    
    @contrapy.check(lambda a, b, _return: a + b == _return, lambda a, b: a < b)
    def demo(a : 22, b : float) -> float:
        return a + b
    
    >>> demo(22, 33.0)
    55.0
    >>> demo(21, 33.0)
    [...]
    ValueError: a should be 22
