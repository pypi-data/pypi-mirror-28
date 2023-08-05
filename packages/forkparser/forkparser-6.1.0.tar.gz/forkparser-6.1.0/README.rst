forkparser - Parse Atom and RSS feeds in Python.

forkparser is a fork of the `kurtmckee/feedparser <https://github.com/kurtmckee/feedparser>`_, which as of January 2018 has not seen a PyPI release in years, despite extensive changes in the ``develop`` branch and numerous worthy pull requests.
Hopefully @kurtmckee will return or pass on maintainership, so I have tried to minimize user-visible divergence.
The forkparser PyPI distribution provides the feedparser Python package, so it can be dropped in instead of feedparser.

The 6.0.0 release includes a number of backwards-incompatible changes as the single-file module has been reorganized into a Python package.
See the NEWS file for more information.

| Copyright 2010-2015 Kurt McKee <contactme@kurtmckee.org>
| Copyright 2002-2008 Mark Pilgrim

feedparser is open source. See the LICENSE file for more information.


Installation
============

forkparser can be installed using Pip by running::

    $ virtualenv parseit
    $ parseit/bin/pip install forkparser

Then parse some feeds::

    $ parseit/bin/python
    >>> import feedparser
    >>> d = feedparser.parse('https://github.com/kurtmckee/feedparser/commits/develop.atom')
    >>> d.feed.title
    u'Recent Commits to feedparser:develop'
    >>> len(d.entries)
    20

Note:

* The `Python packaging user guide <https://packaging.python.org/tutorials/installing-packages/>`_ has more on installing packages with ``pip``.
* sgmllib3k is required on Python 3. It will be installed automatically provided you have a sufficiently recent ``pip``.

Documentation
=============

The feedparser documentation is available on the web at:

    https://pythonhosted.org/feedparser/

It is also included in its source format, ReST, in the docs/ directory. To
build the documentation you'll need the Sphinx package, which is available at:

    http://sphinx.pocoo.org/

You can then build HTML pages using a command similar to::

    $ sphinx-build -b html docs/ fpdocs

This will produce HTML documentation in the fpdocs/ directory.


Testing
=======

Feedparser has an extensive test suite, powered by tox. To run it, type this::

    $ tox

This will spawn an HTTP server that will listen on port 8097. The tests will
fail if that port is in use.
