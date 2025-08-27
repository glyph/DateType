.. DateType documentation master file, created by
   sphinx-quickstart on Sat Apr 12 18:02:01 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DateType documentation
======================

What Is DateType?
-----------------

DateType is a `workaround for this
bug <https://github.com/python/mypy/issues/9015>`_ to demonstrate that we could
have a type-checking-time wrapper for ``datetime`` that doesn't change (or almost
doesn't change) the implementation, but fixes up two very annoying behaviors of
the stdlib ``datetime`` module:


#. 
   a ``datetime`` now won't type-check as a ``date`` - it still inherits at runtime
   (the implementation is, after all, not changed) but it doesn't inherit at
   type-time.

#. 
   there are separate types for naive and aware ``datetime``\ s.

There's a very small bit of implementation glue (concrete ``@classmethod``\ s for
construction on the ``Naive`` and ``Aware`` types, and a few functions that do
runtime checks to convert to/from stdlib types).

What Does It Contain?
---------------------

After you ``pip install datetype``, you can import the ``datetype`` module.

In that module, you will find several types, each of which is a :py:class:`typing.Protocol` that abstractly describes an *existing* type within the standard library.

The first, ``datetype.Date``, is just an abstract description of :py:class:`datetime.date` ; it has all the same methods and attributes.

The other two, ``datetype.Time[TZ]`` and ``datetype.DateTime[TZ]`` are abstract descriptions of :py:class:`datetime.time` and :py:class:`datetime.datetime` respectively, both :py:class:`generic <typing.Generic>` on a timezone type; which is to say, a subclass of :py:class:`datetime.tzinfo`, or ``None``.

In the two places that a timezone is used as a return value in one of these :py:mod:`datetime` types, the equivalent ``datetype`` object's method has its ``TZ`` type precisely, rather than a union.  These are:

1. The ``.tzinfo`` property on both ``DateTime`` and ``Time``, and
2. The ``timetz()`` method on ``DateTime``.

This means that, for example, if you have a ``datetype.DateTime[``\ :py:class:`zoneinfo.ZoneInfo`\ ``]``, you can get its timezone without checking anything, and it will type-check correctly:

.. code-block::
   :language: python

   from datetype import DateTime
   from zoneinfo import ZoneInfo

   def func(dt: DateTime[ZoneInfo]) -> None:
       print(f"This datetime is in the {dt.tzinfo.key} timezone.")

By contrast, the ``datetime`` version of this:

.. code-block::
   :language: python

   from datetime import datetime

   def func(dt: datetime) -> None:
       print(f"This datetime is in the {dt.tzinfo.key} timezone.")

will result in 2 mypy errors:

1. ``Item "tzinfo" of "tzinfo | None" has no attribute "key"``, because the abstract ``tzinfo`` type doesn't let you know that it's a ``zoneinfo.ZoneInfo``, so it won't have ``ZoneInfo``'s custom key attribute, and
2. ``Item "None" of "tzinfo | None" has no attribute "key"``, because the type ``datetime.datetime`` might *always* be a naive datetime with no timezone information at all.

This is how datetype lets you describe your ``datetime`` object to avoid spurious errors when you've already made sure that those objects definitely have a timezone already.

``datetype`` will also help you by reporting errors any time you accidentally mix naive and aware datetimes.

For example, this program will type check cleanly according to ``mypy``, but will result in a runtime ``TypeError: can't subtract offset-naive and offset-aware datetimes``:

.. code-block::

    import datetime

    def seconds_between(then: datetime.datetime, now: datetime.datetime) -> float:
        return (now - then).total_seconds()

    from time import sleep
    a = datetime.datetime.now()
    sleep(2)
    b = datetime.datetime.now(datetime.UTC)
    print(seconds_between(a, b))

The problem here is that a naive datetime and an aware datetime are not actually compatible types, despite sharing the same class in the standard library.  With ``datetype``, you would express this as such:

.. code-block::

    from datetype import DateTime
    from datetime import UTC, tzinfo

    def seconds_between(then: DateTime[tzinfo], now: DateTime[tzinfo]) -> float:
        return (now - then).total_seconds()

    from time import sleep
    a = DateTime.now()
    sleep(2)
    b = DateTime.now(UTC)
    print(seconds_between(a, b))

This version of the program will fail the same way at runtime, but, when checking with ``mypy``, now you will get ``Argument 1 to "seconds_between" has incompatible type "DateTime[None]"; expected "DateTime[tzinfo]"`` while type checking.  If we were to replace ``DateTime[tzinfo]`` with ``DateTime[None]`` to indicate that ``then`` could be a naive datetime, we would instead accurately get the error ``Unsupported operand types for - ("DateTime[tzinfo]" and "DateTime[None]")``.

How Do You Use It?
------------------

One way to use ``datetype`` is already shown in the example above: the classmethod constructors on ``DateTime`` and ``Time`` (i.e.: ``.now(...)``, ``.utcfromtimestamp()``, ``.utcnow()``, ``.fromtimestamp(...)``, ``.combine()``) all have type hints that will give the appropriately specialized type back.  So, when you can use those, it works more or less automatically.

However, in a real Python program, you are almost certainly going to need to deal with libraries whose type hints are in terms of the :py:mod:`datetime` module.  To convert back and forth from those types, ``datetype`` exposes 3 additional functions:

- ``datetype.aware(datetime|time, [type[timezone]:TZ]) -> DateType[TZ]`` : If you have a standard library object ``dt``, you can call ``aware(dt)`` to verify that it has a non-``None`` tzinfo, and get back a ``DateType`` object specialized on that timezone.  If you pass a specific timezone type, it will verify and specialize on that exact type rather than the base ``tzinfo``.
- ``datetype.naive(datetime|time) -> DateType[None]`` : If you have a standard library object with *no* timezone, this will verify that, and return a ``DateType[None]``.
- ``datetype.concrete(datetype.Date | datetype.DateTime | datetype.Time) -> datetime.date | datetime.datetime | datetime.time`` : If you have a ``datetype`` object of some type, this will return it as a ``datetime`` object instead.

Note that *at runtime*, these types are all the exact same classes.  None of these functions actually instantiate anything new.  These conversions merely verify any relevant invariants, then return the abstract type represnting those invariants.

Thus, the way that you use ``datetype`` as a library is to write all the functions in *your* application using these types, and then at the boundaries where you need to interact with existing Python libraries that use the standard library types, you can convert to and from them as described here.

By doing so, you will:

1. prevent spurious runtime errors from accidental mixing of naive and aware ``datetime`` objects, instead getting helpful early warnings from your type checker, and
2. prevent incorrect calculation surprises from accidentally using ``datetime`` objects as ``date`` objects (since ``datetype.Date`` does not type check as a ``datetype.DateTime`` or vice versa).

.. toctree::
   :maxdepth: 2
   :caption: Contents:

