#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Wed Oct 17 15:59:25 CEST 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This file defines simple Client and File interfaces that should be comparable
with other xbob.db databases.
"""

import os
import bob

class Client:
  """The clients of this database contain ONLY client ids. Nothing special."""
  def __init__(self, client_id):
    self.id = client_id


class File:
  """Files of this database are composed from the client id and a file id."""
  file_count_per_id = 10

  def __init__(self, client_id, client_file_id):
    assert client_file_id in range(1, self.file_count_per_id + 1)
    # compute the file id on the fly
    self.id = (client_id-1) * self.file_count_per_id + client_file_id
    # copy client id
    self.client_id = client_id
    # generate path on the fly
    self.path = os.path.join("s" + str(client_id), str(client_file_id))


  def make_path(self, directory=None, extension=None):
    """Wraps the current path so that a complete path is formed

    Keyword parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    extension
      An optional extension that will be suffixed to the returned filename. The
      extension normally includes the leading ``.`` character as in ``.jpg`` or
      ``.hdf5``.

    Returns a string containing the newly generated file path.
    """

    if not directory: directory = ''
    if not extension: extension = ''

    return os.path.join(directory, self.path + extension)


  def save(self, data, directory=None, extension='.hdf5'):
    """Saves the input data at the specified location and using the given
    extension.

    Keyword parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      If not empty or None, this directory is prefixed to the final file
      destination

    extension
      The extension of the filename - this will control the type of output and
      the codec for saving the input blob.
    """

    path = self.make_path(directory, extension)
    bob.utils.makedirs_safe(os.path.dirname(path))
    bob.io.save(data, path)

