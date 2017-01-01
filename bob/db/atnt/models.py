#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


"""
This file defines simple Client and File interfaces that should be comparable
with other bob.db databases.
"""

import os
import bob

import bob.db.base
import bob.io.image  # to be able to load images when File.load is called!


class Client(object):
    """The clients of this database contain ONLY client ids. Nothing special."""
    m_valid_client_ids = set(range(1, 41))

    def __init__(self, client_id):
        super(Client, self).__init__()
        assert client_id in self.m_valid_client_ids
        self.id = client_id


class File (bob.db.base.File):
    """Files of this database are composed from the client id and a file id."""
    m_valid_file_ids = set(range(1, 11))

    def __init__(self, client_id, client_file_id):
        assert client_file_id in self.m_valid_file_ids
        # compute the file id on the fly
        file_id = (client_id - 1) * len(self.m_valid_file_ids) + client_file_id
        # generate path on the fly
        path = os.path.join("s" + str(client_id), str(client_file_id))
        # call base class constructor
        bob.db.base.File.__init__(self, file_id=file_id, path=path)
        self.client_id = client_id

    @staticmethod
    def from_file_id(file_id):
        """Returns the File object for a given file_id"""
        client_id = int((file_id - 1) / len(File.m_valid_file_ids) + 1)
        client_file_id = (file_id - 1) % len(File.m_valid_file_ids) + 1
        return File(client_id, client_file_id)

    @staticmethod
    def from_path(path):
        """Returns the File object for a given path"""
        # get the last two paths
        paths = os.path.split(path)
        file_name = os.path.splitext(paths[1])[0]
        paths = os.path.split(paths[0])
        assert paths[1][0] == 's'
        return File(int(paths[1][1:]), int(file_name))
