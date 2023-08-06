Wraptitude: wrap the results of your Python functions
=====================================================

.. image:: https://img.shields.io/circleci/project/github/brettbeatty/wraptitude.svg
    :target: https://circleci.com/gh/brettbeatty/wraptitude

.. image:: https://img.shields.io/github/license/brettbeatty/wraptitude.svg
    :target: https://github.com/brettbeatty/wraptitude/blob/master/LICENSE

.. image:: https://img.shields.io/codecov/c/github/brettbeatty/wraptitude.svg
    :target: https://codecov.io/gh/brettbeatty/wraptitude

.. image:: https://img.shields.io/pypi/v/wraptitude.svg
    :target: https://pypi.org/project/wraptitude/

Wraptitude provides a decorator that wraps result of a function call in a call to another function.

.. code-block:: python

    >>> from wraptitude import Wrapper
    >>> @Wrapper(dict)
    ... def f(x):
    ...     for i in range(x):
    ...         yield i, i ** 2
    ...
    >>> f(3)
    {0: 0, 1: 1, 2: 4}
    >>> @Wrapper(lambda x, y: x + y, 4)
    ... def g(x):
    ...     return x * 5
    ...
    >>> g(2)
    14
