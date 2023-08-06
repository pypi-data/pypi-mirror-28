Spans
=====
|test-status| |test-coverage| |documentation-status| |pypi-version| |py-versions| |license|

Spans is a pure Python implementation of PostgreSQL's
`range types <http://www.postgresql.org/docs/9.6/static/rangetypes.html>`_.
Range types are convenient when working with intervals of any kind. Every time
you've found yourself working with date_start and date_end, an interval may have
been what you were actually looking for.

Spans has successfully been used in production since its first release
30th August, 2013.


Installation
------------
Spans exists on PyPI.

.. code-block:: bash

    $ pip install Spans

`Documentation <http://spans.readthedocs.org/en/latest/>`_ is hosted on Read the
Docs.


Example
-------
Imagine you are building a calendar and want to display all weeks that overlaps
the current month. Normally you have to do some date trickery to achieve this,
since the month's bounds may be any day of the week. With Spans' set-like
operations and shortcuts the problem becomes a breeze.

We start by importing ``date`` and ``daterange``

.. code-block:: python

    >>> from datetime import date
    >>> from spans import daterange

Using ``daterange.from_month`` we can get range representing January in the year
2000

.. code-block:: python

    >>> month = daterange.from_month(2000, 1)
    >>> month
    daterange([datetime.date(2000, 1, 1),datetime.date(2000, 2, 1)))

Now we can calculate the ranges for the weeks where the first and last day of
month are

.. code-block:: python

    >>> start_week = daterange.from_date(month.lower, period="week")
    >>> end_week = daterange.from_date(month.last, period="week")
    >>> start_week
    daterange([datetime.date(1999, 12, 27),datetime.date(2000, 1, 3)))
    >>> end_week
    daterange([datetime.date(2000, 1, 31),datetime.date(2000, 2, 7)))

Using a union we can express the calendar view.

.. code-block:: python

    >>> start_week.union(month).union(end_week)
    daterange([datetime.date(1999, 12, 27),datetime.date(2000, 2, 7)))

Do you want to know more? Head over to the
`documentation <http://spans.readthedocs.org/en/latest/>`_.


Use with Psycopg2
-----------------
To use these range types with Psycopg2 the
`PsycoSpans <https://www.github.com/runfalk/psycospans>`_.


Motivation
----------
For a project of mine I started using PostgreSQL's ``tsrange`` type and needed
an equivalent in Python. These range types attempt to mimick PostgreSQL's
behavior in every way. Deviating from it is considered as a bug and should be
reported.


Contribute
----------
I appreciate all the help I can get! Some things to think about:

- If it's a simple fix, such as documentation or trivial bug fix, please file
  an issue or submit a pull request. Make sure to only touch lines relevant to
  the issue. I don't accept pull requests that simply reformat the code to be
  PEP8-compliant. To me the history of the repository is more important.
- If it's a feature request or a non-trivial bug, always open an issue first to
  discuss the matter. It would be a shame if good work went to waste because a
  pull request doesn't fit the scope of this project.

Pull requests are credited in the change log which is displayed on PyPI and the
documentaion on Read the Docs.


.. |test-status| image:: https://travis-ci.org/runfalk/spans.svg
    :alt: Test status
    :scale: 100%
    :target: https://travis-ci.org/runfalk/spans

.. |test-coverage| image:: https://codecov.io/github/runfalk/spans/coverage.svg?branch=master
    :alt: Test coverage
    :scale: 100%
    :target: https://codecov.io/github/runfalk/spans?branch=master

.. |documentation-status| image:: https://readthedocs.org/projects/spans/badge/
    :alt: Documentation status
    :scale: 100%
    :target: http://spans.readthedocs.org/en/latest/

.. |pypi-version| image:: https://badge.fury.io/py/Spans.svg
    :alt: PyPI version status
    :scale: 100%
    :target: https://pypi.python.org/pypi/Spans/

.. |py-versions| image:: https://img.shields.io/pypi/pyversions/Spans.svg
    :alt: Python version
    :scale: 100%
    :target: https://pypi.python.org/pypi/Spans/

.. |license| image:: https://img.shields.io/github/license/runfalk/spans.svg
    :alt: MIT License
    :scale: 100%
    :target: https://github.com/runfalk/spans/blob/master/LICENSE

.. Include changelog on PyPI

Changelog
=========
Version are structured like the following: ``<major>.<minor>.<bugfix>``. The
first `0.1` release does not properly adhere to this. Unless explicitly stated,
changes are made by `Andreas Runfalk <https://github.com/runfalk>`_.


Version 1.0.1
-------------
Released on 31st January, 2018

- Fixed ``PartialOrderingMixin`` not using ``__slots__``
  (`bug #10 <https://github.com/runfalk/spans/issues/10>`_)


Version 1.0.0
-------------
Released on 8th June, 2017

- Added ``NotImplemented`` for ``<<`` and ``>>`` operators when there is a type
  mismatch
- Added ``|`` operator for unions of ``Range`` and
  ``NotImplemented`` support for ``RangeSet``
- Added ``&`` operator for intersections of ``Range`` and
  ``NotImplemented`` support for ``RangeSet``
- Added ``-`` operator for differences of ``Range`` and
  ``NotImplemented`` support for ``RangeSet``
- Added ``reversed()`` iterator support for ``DiscreteRange``
- Fixed overlap with empty range incorrectly returns ``True``
  (`bug #7 <https://github.com/runfalk/spans/issues/7>`_)
- Fixed issue with ``contains()`` for scalars on unbounded
  ranges
- Fixed type check for ``right_of()``
- Fixed type check for ``contains()``
- Fixed type check for ``union()``
- Fixed type check for ``intersection()``
- Fixed type check for ``difference()``
- Fixed infinite iterators not being supported for
  ``DiscreteRange``


Version 0.5.0
-------------
Released on 16th April, 2017

This release is a preparation for a stable 1.0 release.

- Fixed comparison operators when working with empty or unbounded ranges. They
  would previously raise exceptions. Ranges are now partially ordered instead of
  totally ordered
- Added more unit tests
- Renamed classes to match `PEP8 <https://www.python.org/dev/peps/pep-0008/#class-names>`_ conventions. This does not apply
  to classes that works on built-in that does not follow `PEP8 <https://www.python.org/dev/peps/pep-0008/#class-names>`_.
- Refactored ``left_of()``
- Refactored ``overlap()``
- Refactored ``union()``


Version 0.4.0
-------------
Released on 20th March, 2017

This release is called 0.4.1 on PyPI because I messed up the upload.

- Added new argument to ``from_date()`` for working
  with different kinds of date intervals. The argument accepts a period of either
  ``"day"`` (default), ``"week"`` (ISO week), ``"american_week"`` (starts on
  sunday), ``"month"``, ``"quarter"`` or ``"year"``.
- Added new methods to ``daterange`` for working with different
  kinds of date intervals:
  ``from_week()``,
  ``from_month()``,
  ``from_quarter()`` and
  ``from_year()``.
- Added a new class ``PeriodRange`` for working with periods
  like weeks, months, quarters or years. It inherits all methods from
  ``daterange`` and is aware of its own period type. It
  allows things like getting the previous or next week.
- Fixed ``daterange`` not accepting subclasses of ``date``
  (`bug #5 <https://github.com/runfalk/spans/issues/5>`_)
- Fixed some broken doctests
- Moved unit tests to `pytest <http://docs.pytest.org/en/latest/>`_
- Removed `Tox <https://tox.readthedocs.io/en/latest/>`_ config
- Minor documentation tweaks


Version 0.3.0
-------------
Released on 26th August, 2016

- Added documentation for ``__iter__()``
- Fixed intersection of multiple range sets not working correctly
  (`bug #3 <https://github.com/runfalk/spans/issues/3>`_)
- Fixed iteration of ``RangeSet`` returning an empty range
  when ``RangeSet`` is empty
  (`bug #4 <https://github.com/runfalk/spans/issues/4>`_)

.. warning::
   This change is backwards incompatible to code that expect range sets to
   always return at least one set when iterating.


Version 0.2.1
-------------
Released on 27th June, 2016

- Fixed ``RangeSet`` not returning ``NotImplemented`` when
  comparing to classes that are not sub classes of ``RangeSet``, pull request
  `#2 <https://github.com/runfalk/spans/pull/2>`_
  (`Michael Krahe <https://github.com/der-michik>`_)
- Updated license in ``setup.py`` to follow
  `recommendations <https://packaging.python.org/en/latest/distributing/#license>`_
  by PyPA


Version 0.2.0
-------------
Released on 22nd December, 2015

- Added ``__len__()`` to range sets
  (`Michael Krahe <https://github.com/der-michik>`_)
- Added ``contains()`` to range sets
  (`Michael Krahe <https://github.com/der-michik>`_)
- Added `Sphinx <http://sphinx-doc.org/>`_ style doc strings to all methods
- Added proper Sphinx documentation
- Added unit tests for uncovered parts, mostly error checking
- Added `wheel <https://www.python.org/dev/peps/pep-0427/>`_ to PyPI along with
  source distribution
- Fixed a potential bug where comparing ranges of different types would result
  in an infinite loop
- Changed meta class implementation for range sets to allow more mixins for
  custom range sets


Version 0.1.4
-------------
Released on 15th May, 2015

- Added ``.last`` property to
  ``DiscreteRange``
- Added ``from_date()`` helper to
  ``daterange``
- Added more unit tests
- Improved pickle implementation
- Made type checking more strict for date ranges to prevent ``datetime`` from
  being allowed in ``daterange``


Version 0.1.3
-------------
Released on 27th February, 2015

- Added ``offset()`` to some range types
- Added ``offset()`` to some range set
  types
- Added sanity checks to range boundaries
- Fixed incorrect ``__slots__`` usage, resulting in ``__slots__`` not being used
  on most ranges
- Fixed pickling of ranges and range sets
- Simplified creation of new range sets, by the use of the meta class
  ``MetaRangeSet``


Version 0.1.2
-------------
Released on 13th June, 2014

- Fix for inproper version detection on Ubuntu's bundled Python interpreter


Version 0.1.1
-------------
Released on 12th June, 2014

- Readme fixes
- Syntax highlighting for PyPI page


Version 0.1.0
-------------
Released on 30th August, 2013

- Initial release


