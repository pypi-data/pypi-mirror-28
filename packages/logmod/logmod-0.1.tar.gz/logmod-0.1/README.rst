logmod
======

Log all calls to a module

Dependencies
------------

- structlog

Features
--------

- Log all calls to a module

Example
-------

.. code:: python

    >>> from logmod import logmod
    >>> import secrets
    >>> logmod(secrets)
    >>>
    >>> secret.token_hex(5)
    logmod: call to secret.token_hex with (5,) {}
    'd34eb399f8'

Results in:

.. code:: text

    2018-01-09 01:04.15 coolname -> secrets.token_hex at example.py:8 args=(5,) caller=coolname callsite={'filename': 'example.py', 'lineno': 8} func=token_hex kwargs={} mod=secrets
    2018-01-09 01:04.15 token_hex -> secrets.token_bytes at /usr/lib/python3.6/secrets.py:58 args=(5,) caller=token_hex callsite={'filename': '/usr/lib/python3.6/secrets.py', 'lineno': 58} func=token_bytes kwargs={} mod=secrets
    Hello, f717fd2370
    2018-01-09 01:04.15 <module> -> random at example.py:12 args=() caller=<module> callsite={'filename': 'example.py', 'lineno': 12} func=random kwargs={} mod=None
    0.46899158604445124
