#################################################
Helpers for Dealing with ``datetime``\s in Lektor
#################################################

************
Introduction
************

This is a plugin for Lektor which provides some helpers for dealing with
dates and times.

Currently this provides a ``dateordatetime`` model field type which
can contain either a ``date`` or a ``datetime``.

Also the following jinja filters are provided:

isoformat(dt)
   Returns an iso formatted version the datetime, with timezone information.
   If ``dt`` is naive, it is localized to the site's default timezone.

localize_datetime(dt)
   If ``dt`` is naive, it is localized to the site's default timezone.


*********
Changelog
*********

Release 0.3 (2018-01-18)
========================

Fix things so that date and datetime types returned by the ``dateordatetime`` Lektor type are comparable against ``None``.  (``None`` compares less than all other dates and datetimes.)


Release 0.2 (2017-08-04)
========================

New features
------------

Make lists of ``dateordatetime`` types sortable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``dateordatetime`` custom Lektor type now returns subclasses of ``datetime.date`` or ``datetime.datetime`` which can be compared against one another.  Normally, attempts to compare a ``date`` against a ``datetime`` results in a ``TypeError`` being raised.  This made it difficult to sort on ``dateordatetime`` values.

Now ``date``\s sort before any ``datetime``\s with the same date.  Naïve ``datetime``\s sort before timezone-aware ``datetime``\s with the same date.

Release 0.1 (2017-04-19)
========================

Initial release.


