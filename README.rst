.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 11:17:03 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.atnt/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.atnt/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.atnt/badges/v2.0.7/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.atnt/commits/v2.0.7
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.atnt
.. image:: http://img.shields.io/pypi/v/bob.db.atnt.png
   :target: https://pypi.python.org/pypi/bob.db.atnt
.. image:: http://img.shields.io/pypi/dm/bob.db.atnt.png
   :target: https://pypi.python.org/pypi/bob.db.atnt


=================================
 AT&T Database Interface for Bob
=================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains an interface for the evaluation protocol of the `AT&T`_
database, formerly known as the ORL database of faces. This package does not
contain the original `AT&T`_ data files, which need to be obtained through the
link above.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel
.. _at&t: http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html
