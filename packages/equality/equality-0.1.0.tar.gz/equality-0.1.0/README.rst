equality
========

Utilities to aid in testing for equality.

|Travis Test Status|

This package is pre-alpha. The API may change.

When comparing structures like this dict::

    assert actual == {
        'id': 123,
        'created': "2017-11-10T23:59:58",
        'field1': 1,
        ...
    }

This fails because 'id' and 'created' are different every test run.
Fix this using::

    assert actual == {
        'id': AnyInt(),
        'created': AnyTimestamp(datetime.now(), seconds=3),
        'field1': 1,
        ...
    }

:code:`AnyInt` compares equal to any integer. :code:`Timestamp` compares equal
to string timestamps that are within the given number of seconds.


Compatibility
-------------

Python 3.6 and 2.7.


Known Problems
--------------

If timestamps are generated locally, in-process, then it's easier to
patch out datetime.now(). But if this is an end-to-end test that hits
other services, that might not be an option. That's when I find AnyTimestamp
useful.

This is all hot off the press, so is doubtless full of mistakes.


Alternatives
------------

This doubtless duplicates better work elsewhere. In particular the package
'equals' looks very nice, but it's missing the central feature of 'equality',
approximate comparison of string timestamps.


Contact
-------

| Users' downloads & documentation: http://pypi.python.org/pypi/equality/
| Contributors' souce & issues: https://github.com/tartley/equality/
| Author: Jonathan Hartley, email: tartley at domain tartley.com, Twitter: @tartley.


.. |Travis Test Status| image:: https://travis-ci.org/tartley/equality.svg?branch=master
    :target: https://travis-ci.org/tartley/equality

