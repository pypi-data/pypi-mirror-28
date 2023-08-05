#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright (c) 2017 Jesse Pinnell
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Test cases for classes in exercise_database.py """

import unittest
from xrsrv import exercise_database
from xrsrv import type_factories

TEST_DATABASE_NAME = "exercise.db"

class TestExcerciseDatabase(unittest.TestCase):
    """
    Test the exercise database methods

    TODO(jessepinnell) refactor or make these more robust tests
    """

    def __init__(self, *args, **kwargs):
        super(TestExcerciseDatabase, self).__init__(*args, **kwargs)
        self.database = exercise_database.Connection(TEST_DATABASE_NAME)

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.database, exercise_database.Connection)

    def test_get_list_of_exercise_names(self):
        """ Test the get_list_of_exercise_names() method """
        self.assertNotEqual(self.database.get_list_of_exercise_names(), False)

    def test_get_muscles(self):
        """ Test the get_muscles() method """
        self.assertNotEqual(self.database.get_muscles(), False)

    def test_get_exercise_data(self):
        """ Test the get_muscles_exercised() method """
        exercises = self.database.get_list_of_exercise_names()
        self.assertNotEqual(exercises, False)
        self.assertIsInstance(self.database.get_exercise_data(exercises[0]),\
            type_factories.Exercise)

if __name__ == '__main__':
    unittest.main()
