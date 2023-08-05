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

""" Abstraction of sqlite3 database """

# TODO(jessepinnell) This should be a pure virtual persistence object
#    with an sqlite3 implementation; refactor it

import sqlite3

# TODO(jessepinnell) figure out why lint doesn't like pathlib
# pylint: disable=import-error
from pathlib import Path

from xrsrv import type_factories

class Connection(object):
    """
    Abstraction of a sqllite3 database
    """
    database_connection = None

    def __init__(self, database_name):
        # Because this will create a database if it doesn't find one explicitly check for one
        existing_db_file = Path(database_name)
        if not existing_db_file.exists():
            raise IOError("Database file doesn't exist: " + database_name)

        self.database_connection = sqlite3.connect(database_name)
        self.cursor = self.database_connection.cursor()

    def get_uids(self, search):
        """
        Find matching uids
        """
        self.cursor.execute("SELECT UID FROM UserProfiles WHERE Name LIKE (?)", (search, ))
        return {i[0] for i in self.cursor.fetchall()}

    def get_user_profile(self, uid):
        """
        Get user profile by UID
        """
        self.cursor.execute("SELECT UID, Name, Notes FROM UserProfiles WHERE UID = ?", (uid,))
        return type_factories.UserProfile._make(self.cursor.fetchone())

    def get_user_fixtures(self, uid):
        """
        Get set of fixtures by UID
        """
        self.cursor.execute("SELECT Name, MinSetting, MaxSetting FROM UserFixtures WHERE UID = ?", (uid,))
        return list(map(type_factories.UserFixture._make, self.cursor.fetchall()))

    def get_user_rigs(self, uid):
        """
        Get set of rigs by UID
        """
        self.cursor.execute("SELECT Name, MinSetting, MaxSetting FROM UserRigs WHERE UID = ?", (uid, ))
        return list(map(type_factories.UserRig._make, self.cursor.fetchall()))

    # TODO(jessepinnell) probably add a limit
    def get_exercise_set_history(self, uid):
        """
        Get the set history by UID
        """
        self.cursor.execute("SELECT ExerciseName, Duration, Setting, Time FROM "
                            "ExerciseSetHistory WHERE UID = ?", (uid, ))
        return list(map(type_factories.ExerciseSet._make, self.cursor.fetchall()))

    def add_to_exercise_set_history(self, uid, exercise_set):
        """
        Get the set history by UID
        """
        if not isinstance(exercise_set, list):
            exercise_set = [exercise_set]

        # executemany would be nice here, but the UID isn't part of exercise_set
        for this_set in exercise_set:
            self.cursor.execute("INSERT INTO ExerciseSetHistory(UID, ExerciseName, Duration, "
                                "Setting, Time) VALUES (?, ?, ?, ?, ?)",\
                (uid, this_set.name, this_set.duration, this_set.setting, this_set.time))
        self.database_connection.commit()


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()
