.. vim: set fileencoding=utf-8 :

.. testsetup:: interface

   import tempfile
   from bob.db.atnt.driver import download
   from bob.db.atnt.models import DEFAULT_DATADIR
   class Arguments(object): pass
   args = Arguments()
   setattr(args, 'output_dir', DEFAULT_DATADIR)
   setattr(args, 'quiet', True)
   assert download(args) == 0


==============
 User's Guide
==============

This package contains the access API and descriptions for the `AT&T`_ database
of faces, which is formerly known as the ORL database. This package only
contains the Bob_ accessor methods to use the dataset directly from python. The
actual raw data for the database should be downloaded from the original URL. A
convenient command is provided for this purpose:

.. code-block:: sh

   $ bob_dbmanage.py atnt download


This command will try to download and install the database on a directory that
is internal to the package. In case you don't have write access to such
directory, use the ``--output-dir`` flag to specify an alternate directory:


.. code-block:: sh

   $ bob_dbmanage.py atnt download --output-dir raw


The command above will download the raw data files of the AT&T database into
the directory ``raw`` inside your current working directory.


The Database Interface
----------------------

The :py:class:`bob.db.atnt.Database` provides an interface to access samples
from this dataset. The database object is initialized by passing it the
location where the raw samples have been downloaded. Assuming downloading to
the package inner directory worked for you, then you don't need to pass any
parameter to the constructor:


.. doctest:: interface

   >>> import bob.db.atnt
   >>> db = bob.db.atnt.Database()

You can then use the :py:meth:`bob.db.atnt.Database.objects` to access
*pointers* to the raw data samples of the AT&T dataset in a programmatic way:


.. doctest:: interface

   >>> for sample in db.objects():
   ...     # do something with "sample"
   ...     pass


In the case of this database, each "sample" returned by
:py:meth:`bob.db.atnt.Database.objects` is actually an object of class
:py:class:`bob.db.atnt.File`, representing the abstraction of a single (raw)
dataset file. File objects in this package contain a ``path`` variable that
point to their relative location w.r.t. a database root directory:

.. doctest:: interface

   >>> f = db.objects()[0]
   >>> type(f) #doctest: +ELLIPSIS
   <... 'bob.db.atnt.models.File'>
   >>> f.path # doctest: +ELLIPSIS
   '...'


You may use the method :py:meth:`bob.db.atnt.File.make_path` to construct paths
which contain both a prefix directory and a suffixed extension. For example, to
build a full path to an installed image in the raw dataset, call this method
without any parameters:

.. code-block:: python

   >>> f.make_path()
   '/install/path/s1/9.pgm'


You may override the default directory and extensions that are attached to the
return path. For example:

.. doctest:: interface

   >>> f.make_path('/another/path', '.hdf5') #doctest: +ELLIPSIS
   '/another/path/....hdf5'

You may load the contents of the image file pointed by this database entry
using the :py:meth:`bob.db.atnt.File.load` method:

.. doctest:: interface

   >>> image = f.load()
   >>> type(image) #doctest: +ELLIPSIS
   <... 'numpy.ndarray'>
   >>> image.shape
   (112, 92)
   >>> image.dtype
   dtype('uint8')


Pipelines
=========

In data processing pipelines, it is typical to save the intermediate result of
processing images to temporary files you'll need to load later. In Bob, those
files are normally HDF5 files (see :ref:`bob.io.base`). You can easily create a
processing pipeline re-using the database interface like this:

.. code-block:: python
   :linenos:

   >>> image = f.load()
   >>> processed = processor(image)
   >>> f.save(processed, '/path/to/processed', '.hdf5')
   # stores "processed" in an HDF5 file file named /path/to/processed/s1/9.hdf5

Line 1 loads the image. Line 2 processes the image and generates a processed
version of the image (e.g. as a :py:class:`numpy.ndarray`). Line 3 above uses
this db package interface to save the resulting file *respecting* the original
database structure. This is convenient because of two reasons:

1. You can manually inspect the directory containing processed images and
   quickly find the processed version of any original image in the database;
2. You can re-use :py:meth:`bob.db.atnt.File.load` to reload the processed file
   and continue the pipelining indefinitely.

For example, suppose one would like to re-process the processed image above, it
is possible to repeat the coding pattern above, now defining input and output
directories:

.. code-block:: python

   >>> processed = f.load('/path/to/processed', '.hdf5')
   >>> reprocessed = reprocessor(processed)
   >>> f.save(processed, '/path/to/reprocessed', '.hdf5')


Selectors
=========

You may iterate over a subset of samples from the AT&T database using
parameters to :py:meth:`bob.db.atnt.Database.objects` (check its documentation
for details). For example, to iterate over all the training images, one can
write:

.. doctest:: interface

   >>> training_images = []
   >>> for sample in db.objects(groups='world'):
   ...   training_images.append(sample.load())


Command-line Interface
----------------------

The command-line interface allows users to check or export information encoded
in Python API via the console. Consult the command-line help for more details:

.. code-block:: sh

   $ bob_dbmanage.py atnt --help
   ...


.. _at&t: http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html
.. _bob: https://www.idiap.ch/software/bob
