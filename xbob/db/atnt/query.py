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

from .models import Client, File

class Database(object):
  """Wrapper class for the AT&T (aka ORL) database of faces (http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html).
  This class defines a simple protocol for training, enrollment and probe by splitting the few images of the database in a reasonable manner.
  Due to the small size of the database, there is only a 'dev' group, and I did not define an 'eval' group."""

  def __init__(self):
    self.m_groups = ('world', 'dev')
    self.m_purposes = ('enrol', 'probe')
    self.m_client_ids = set(range(1, 41))
    self.m_files = set(range(1, 11))
    self.m_training_clients = set([1,2,5,6,10,11,12,14,16,17,20,21,24,26,27,29,33,34,36,39])
    self.m_enrol_files = set([2,4,5,7,9])


  def __check_validity__(self, l, obj, valid, default):
    """Checks validity of user input data against a set of valid values."""
    if not l: return default
    elif isinstance(l, str) or isinstance(l, int): return self.__check_validity__([l], obj, valid, default)
    for k in l:
      if k not in valid:
        raise RuntimeError, 'Invalid %s "%s". Valid values are %s, or lists/tuples of those' % (obj, k, valid)
    return l


  def clients(self, groups = None, protocol = None):
    """Returns the vector of clients used in a given group

    Keyword Parameters:

    groups
      One of the groups 'world', 'dev' or a tuple with both of them (which is the default).

    protocol
      Ignored.
    """

    VALID_GROUPS = self.m_groups
    groups = self.__check_validity__(groups, "group", VALID_GROUPS, VALID_GROUPS)

    ids = set()
    if 'world' in groups:
      ids |= self.m_training_clients
    if 'dev' in groups:
      ids |= self.m_client_ids - self.m_training_clients

    return [Client(id) for id in ids]

  def client_ids(self, groups = None, protocol = None):
    """Returns the vector of ids of the clients used in a given group

    Keyword Parameters:

    groups
      One of the groups 'world', 'dev' or a tuple with both of them (which is the default).

    protocol
      Ignored.
    """

    VALID_GROUPS = self.m_groups
    groups = self.__check_validity__(groups, "group", VALID_GROUPS, VALID_GROUPS)

    ids = set()
    if 'world' in groups:
      ids |= self.m_training_clients
    if 'dev' in groups:
      ids |= self.m_client_ids - self.m_training_clients

    return sorted(list(ids))


  def models(self, groups = None, protocol = None):
    """Returns the vector of models ( == clients ) used in a given group

    Keyword Parameters:

    groups
      One of the groups 'world', 'dev' or a tuple with both of them (which is the default).

    protocol
      Ignored.
    """

    return self.clients(groups, protocol)


  def model_ids(self, groups = None, protocol = None):
    """Returns the vector of ids of the models (i.e., the client ids) used in a given group

    Keyword Parameters:

    groups
      One of the groups 'world', 'dev' or a tuple with both of them (which is the default).

    protocol
      Ignored.
    """

    return self.client_ids(groups, protocol)


  def get_client_id_from_file_id(self, file_id):
    """Returns the client id from the given image id"""
    return (file_id-1) / len(self.m_files) + 1


  def get_client_id_from_model_id(self, model_id):
    """Returns the client id from the given model id"""
    return model_id


  def objects(self, model_ids=None, groups=None, purposes=None, protocol=None):
    """Returns a set of File objects for the specific query by the user.

    Keyword Parameters:

    model_ids
      The ids of the clients whose files need to be retrieved. Should be a list of integral numbers from [1,40]

    groups
      One of the groups 'world' or 'dev' or a list with both of them (which is the default).

    purposes
      One of the purposes 'enrol' or 'probe' or a list with both of them (which is the default).
      This field is ignored when the group 'world' is selected.

    protocol
      Ignored.

    Returns: A list of File's considering all the filtering criteria.
    """

    # check if groups set are valid
    VALID_GROUPS = self.m_groups
    groups = self.__check_validity__(groups, "group", VALID_GROUPS, VALID_GROUPS)

    # collect the ids to retrieve
    ids = set(self.client_ids(groups))

    # check the desired client ids for sanity
    VALID_IDS = self.m_client_ids
    model_ids = self.__check_validity__(model_ids, "model", VALID_IDS, VALID_IDS)

    # calculate the intersection between the ids and the desired client ids
    ids = ids & set(model_ids)

    # check that the groups are valid
    VALID_PURPOSES = self.m_purposes
    if 'dev' in groups:
      purposes = self.__check_validity__(purposes, "purpose", VALID_PURPOSES, VALID_PURPOSES)
    else:
      purposes = VALID_PURPOSES


    # go through the dataset and collect all desired files
    retval = []
    if 'enrol' in purposes:
      for client_id in ids:
        for file_id in self.m_enrol_files:
          retval.append(File(client_id, file_id))

    if 'probe' in purposes:
      file_ids = self.m_files - self.m_enrol_files
      # for probe, we use all clients of the given groups
      for client_id in self.client_ids(groups):
        for file_id in file_ids:
          retval.append(File(client_id, file_id))

    return retval


