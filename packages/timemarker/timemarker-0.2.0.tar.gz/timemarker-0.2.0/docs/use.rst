Usage
======

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
