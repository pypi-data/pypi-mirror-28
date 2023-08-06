|Travis|_ |Coveralls|_ |Docs|_

.. |Travis| image:: https://api.travis-ci.org/davidr/python-timemarker.png?branch=master
.. _Travis: https://travis-ci.org/davidr/python-timemarker

.. |Coveralls| image:: https://coveralls.io/repos/davidr/python-timemarker/badge.png?branch=master
.. _Coveralls: https://coveralls.io/r/davidr/python-timemarker?branch=master

.. |Docs| image:: https://readthedocs.org/projects/python-timemarker/badge/?version=latest
.. _Docs: http://python-timemarker.readthedocs.org/en/latest/

python-timemarker
=================

Simple timer marker for python

Basically something I was using for another project and decided to make it a test project for all
the fancypants integrations like travis, coveralls, rtd, etc.

Usage
-----

To use a simple timemarker:

.. code-block:: python

    import timemarker
    with timemarker.TimeMarker() as t:
        t.tag("something")
        do_something()

        t.tag("some_other_thing")
        do_some_other_thing()

    t.stats()

Examples
--------

>>> with timemarker.TimeMarker() as t:
>>>     t.tag("something")
>>>     do_something()
>>>     t.tag("some_other_thing")
>>>     do_some_other_thing()
>>>
>>> t.stats()
TIME:0.200902s something:0.500 some_other_thing:0.500 start:0.000
