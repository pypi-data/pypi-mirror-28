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

    This essentially acts as an object factory for the data structures,
    converting the data into the tables into more easily usable objects.
    """
    database_connection = None

    def __init__(self, database_name):
        # Because this will create a database if it doesn't find one,
        # explicitly check for one
        existing_db_file = Path(database_name)
        if not existing_db_file.exists():
            raise IOError("Database file doesn't exist: " + database_name)

        self.database_connection = sqlite3.connect(database_name)
        self.cursor = self.database_connection.cursor()


    def get_list_of_exercise_names(self):
        """
        Get a list of the exercises in the database
        """
        self.cursor.execute("SELECT Name FROM Exercises")
        exercise_names = [i[0] for i in self.cursor.fetchall()]
        return exercise_names


    def get_muscles(self):
        """
        Get set of muscles
        """
        self.cursor.execute("SELECT Name, MuscleGroup, Info FROM Muscles")
        return map(type_factories.Muscle._make, self.cursor.fetchall())


    def get_exercise_data(self, name):
        """
        Get the full set of data for a given exercise
        """
        # pylint: disable=no-member
        self.cursor.execute(\
            "SELECT FixtureName FROM ExerciseFixtures WHERE ExerciseName = ?", (name, ))
        fixtures = {i[0] for i in self.cursor.fetchall()}

        self.cursor.execute(\
            "SELECT RigName, Optional FROM ExerciseRigs WHERE ExerciseName = ?", (name, ))
        rigs = list(map(type_factories.ExerciseRig._make, self.cursor.fetchall()))

        self.cursor.execute(\
            "SELECT Muscle FROM MusclesExercised WHERE ExerciseName = ?", (name, ))
        muscles_exercised = [i[0] for i in self.cursor.fetchall()]

        self.cursor.execute(\
            "SELECT Key, Value FROM ExerciseInfo WHERE ExerciseName = ?", (name, ))
        info = {key: value for (key, value) in self.cursor.fetchall()}

        return type_factories.Exercise(name, fixtures, rigs, muscles_exercised, info)


    def __del__(self):
        if self.database_connection is not None:
            self.database_connection.close()
