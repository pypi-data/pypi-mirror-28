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

""" Test cases for classes in user_database.py """
# pylint: disable=invalid-name

import unittest
from xrsrv import user_database
from xrsrv import type_factories

TEST_DATABASE_NAME = "user.db"

class TestUserDatabase(unittest.TestCase):
    """
    Test the user database methods

    TODO(jessepinnell) refactor or make these more robust tests
    """

    def __init__(self, *args, **kwargs):
        super(TestUserDatabase, self).__init__(*args, **kwargs)
        self.database = user_database.Connection(TEST_DATABASE_NAME)

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.database, user_database.Connection)

    def test_get_uids(self):
        """ Test the get_uids() method """
        uids = self.database.get_uids("%")
        self.assertEqual(len(uids), 1)
        self.assertIn(8675309, uids)

        uids = self.database.get_uids("Test User")
        self.assertEqual(len(uids), 1)
        self.assertIn(8675309, uids)

        uids = self.database.get_uids("Test%")
        self.assertEqual(len(uids), 1)
        self.assertIn(8675309, uids)

        uids = self.database.get_uids("bleh")
        self.assertEqual(len(uids), 0)

    def test_get_user_profile(self):
        """ Test the get_user_profile() method """
        # false positive for profile.name
        # pylint: disable=no-member
        uids = self.database.get_uids("%")
        profile = self.database.get_user_profile(uids.pop())
        self.assertEqual(profile.name, "Test User")

    def test_get_user_fixtures(self):
        """ Test the get_user_fixtures() method """
        uids = self.database.get_uids("%")
        fixtures = self.database.get_user_fixtures(uids.pop())
        names = [fixture.name for fixture in fixtures]
        max_settings = [fixture.max_setting for fixture in fixtures]
        self.assertEqual(len(names), 5)
        self.assertIn("test_fixture_1_", names)
        self.assertIn("test_fixture_2a_", names)
        self.assertIn("test_fixture_2b_", names)
        self.assertIn("test_fixture_3_", names)
        self.assertIn("test_fixture_4_", names)
        self.assertIn(0, max_settings)
        self.assertIn(100, max_settings)

    def test_get_user_rigs(self):
        """ Test the get_user_rigs() method """
        uids = self.database.get_uids("%")
        rigs = self.database.get_user_rigs(uids.pop())
        names = [rig.name for rig in rigs]
        min_settings = [rig.min_setting for rig in rigs]
        max_settings = [rig.max_setting for rig in rigs]
        self.assertEqual(len(names), 4)
        self.assertIn("test_rig_1_", names)
        self.assertIn("test_rig_2_", names)
        self.assertIn("test_rig_3_", names)
        self.assertIn("test_rig_4_", names)
        self.assertIn(25, min_settings)
        self.assertIn(55, min_settings)
        self.assertIn(200, max_settings)
        self.assertIn(135, max_settings)

    def test_get_exercise_set_history(self):
        """ Test the get_exercise_set_history() method """
        uids = self.database.get_uids("%")
        exercise_sets = self.database.get_exercise_set_history(uids.pop())
        names = [this_set.name for this_set in exercise_sets]
        self.assertEqual(names.count("test_exercise_4_"), 9)

    def test_add_to_exercise_set_history(self):
        """ Test the add_to_exercise_set_history() method using a single ExerciseSet """
        # pylint: disable=no-member
        uids = self.database.get_uids("%")

        in_set = type_factories.ExerciseSet._make(["test_exercise_5_", 999, 1234, "2017-12-10 20:23:50.000"])
        self.database.add_to_exercise_set_history(8675309, in_set)
        out_sets = self.database.get_exercise_set_history(uids.pop())
        names = [this_set.name for this_set in out_sets]
        settings = [this_set.setting for this_set in out_sets]
        durations = [this_set.duration for this_set in out_sets]
        self.assertIn(in_set.name, names)
        self.assertIn(in_set.duration, durations)
        self.assertIn(in_set.setting, settings)

    def test_add_to_exercise_set_history_set(self):
        """ Test the add_to_exercise_set_history() method using a list of ExerciseSets """
        # pylint: disable=no-member
        uids = self.database.get_uids("%")
        in_sets = [type_factories.ExerciseSet._make(["test_exercise_6_", 999, 1234, "2017-12-10 20:23:50.000"]),
                   type_factories.ExerciseSet._make(["test_exercise_7_", 999, 1234, "2017-12-10 20:23:50.000"]),
                   type_factories.ExerciseSet._make(["test_exercise_8_", 999, 1234, "2017-12-10 20:23:50.000"])]
        self.database.add_to_exercise_set_history(8675309, in_sets)
        out_sets = self.database.get_exercise_set_history(uids.pop())
        names = {this_set.name for this_set in out_sets}
        in_names = {this_set.name for this_set in in_sets}
        self.assertTrue(in_names.issubset(names))


if __name__ == '__main__':
    unittest.main()
