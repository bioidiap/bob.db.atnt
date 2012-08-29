#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A few checks at the AT&T/ORL Face database.
"""

import os, sys
import unittest
from . import Database

class ATNTDatabaseTest(unittest.TestCase):
  """Performs various tests on the AT&T/ORL Face database."""

  def test01_query(self):
    db = Database()
    
    f = db.files()
    self.assertEqual(len(f.values()), 400) # number of all files in the database

    f = db.files(groups='world')
    self.assertEqual(len(f.values()), 200) # number of all training files
   
    f = db.files(groups='dev')
    self.assertEqual(len(f.values()), 200) # number of all test files
    
    f = db.files(groups='dev', purposes = 'enrol')
    self.assertEqual(len(f.values()), 100) # number of enrol files

    f = db.files(groups='dev', purposes = 'probe')
    self.assertEqual(len(f.values()), 100) # number of probe files

    f = db.clients()
    self.assertEqual(len(f), 40) # number of clients
    
    f = db.clients(groups = 'world')
    self.assertEqual(len(f), 20) # number of training clients

    f = db.clients(groups = 'dev')
    self.assertEqual(len(f), 20) # number of test clients

    f = db.files(groups = 'dev', purposes = 'enrol', client_ids = [3])
    self.assertEqual(len(f), 5)
    keys = sorted(f.keys())
    values = sorted(list(db.m_enrol_files))
    for i in range(5):
      self.assertEqual(f[keys[i]], os.path.join("s3", str(values[i])))
      self.assertEqual(db.get_client_id_from_file_id(keys[i]), 3)


  def test02_manage_dumplist_1(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('atnt dumplist --self-test'.split()), 0)

  def test03_manage_checkfiles(self):

    from bob.db.script.dbmanage import main

    self.assertEqual(main('atnt checkfiles -d "." --self-test'.split()), 0)