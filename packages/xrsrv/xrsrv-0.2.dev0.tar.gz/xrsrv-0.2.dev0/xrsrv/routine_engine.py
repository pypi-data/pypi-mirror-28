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

"""
This module contains the class(es) which process user profile data and generates
exercise routines

1) determine what exercises are available based on equipment
2) set user history
3) callers select generation routine and feed it that information
4) the routine generators generate lists of exercises meeting requirements
"""

# TODO Add logging
# pylint: disable=too-many-branches

from xrsrv import exercise_database
from xrsrv.type_factories import RoutineEnvironment

import xrsrv.routine_generators.debug
import xrsrv.routine_generators.basic_random
import xrsrv.routine_generators.multi_day_random

class EngineException(Exception):
    """ Routine engine exception class """
    def __init__(self, value):
        super(EngineException, self).__init__()
        self.value = value

    def __str__(self):
        return self.value

class RoutineEngine(object):
    """ Routine engine """
    def __init__(self, exercise_database_name):
        self.exercise_database = exercise_database.Connection(exercise_database_name)
        self.user_routine_history = []
        self.user_preferences = None
        self.available_exercises = set()
        self.unavailable_exercises = set()
        self.exercise_data = {exercise: self.exercise_database.get_exercise_data(exercise)\
                for exercise in self.exercise_database.get_list_of_exercise_names()}
        self.generators = {
            "debug": xrsrv.routine_generators.debug,
            "basic_random": xrsrv.routine_generators.basic_random,
            "multi_day_random": xrsrv.routine_generators.multi_day_random
        }


    def set_user_exercise_environment(self, user_fixtures, user_rigs, verbose=False):
        """ set the user environment to use for generation functions

        if len(user_fixtures) = 0, give all exercises possible
        """
        print_verbose = print if verbose else lambda *a, **k: None

        self.available_exercises = set()
        self.unavailable_exercises = set()

        # Starting with the full list of exercise choices, remove or use them depending on
        # whether they pass all the rules tests
        for exercise_name, exercise in self.exercise_data.items():
            # *** Fixture checks ***
            if not user_fixtures:
                print_verbose("Y: No user fixtures supplied, adding by default: " + exercise_name)
                self.available_exercises.add(exercise_name)
                continue

            #Check if the user has any fixture satisfying this exercise
            #if count(exercise_fixtures) > 1 then any single fixture can be used
            if user_fixtures and exercise.fixtures.intersection({uf.name for uf in user_fixtures}):
                # User had the fixture, check rigs

                if exercise.rigs:
                    exercise_rig_names = {rig.name for rig in exercise.rigs}
                    user_rig_names = {rig.name for rig in user_rigs}

                    # If count(exercise_rigs) > 0 and all are optional, then any single one or none can be used
                    optional_values = [rig.optional for rig in exercise.rigs]
                    if optional_values and all(optional_values):
                        print_verbose("Y: All rigs are optional ({0}), adding {1}".format(exercise.rigs, exercise_name))
                        self.available_exercises.add(exercise_name)
                        continue

                    # If count(exercise_rigs) > 1 and all are not optional, then any single one can be used
                    if len(exercise_rig_names) == 1:
                        if exercise_rig_names.issubset(user_rig_names):
                            print_verbose("Y: Has the single required rig ({0}), adding {1}".format(\
                                    *exercise_rig_names, exercise_name))
                            self.available_exercises.add(exercise_name)
                            continue
                        else:
                            print_verbose("N: User doesn't have the rig ({0}), skipping {1}".format(\
                                *exercise_rig_names, exercise_name))
                            self.unavailable_exercises.add(exercise_name)
                            continue

                    else: # assume > 1
                        required_rig_names = {rig.name for rig in exercise.rigs if not rig.optional}
                        if user_rig_names.intersection(required_rig_names):
                            print_verbose("Y: Has more than one that work as the required rig ({0}), adding {1}"\
                                .format(user_rig_names.intersection(required_rig_names), exercise_name))
                            self.available_exercises.add(exercise_name)
                            continue
                        else:
                            print_verbose("N: User doesn't have any rigs ({0}) that work for {1}".format(\
                                *required_rig_names, exercise_name))
                            self.unavailable_exercises.add(exercise_name)
                            continue

                else:
                    print_verbose("Y: User has fixture and exercise requires no rigs, adding " + exercise_name)
                    self.available_exercises.add(exercise_name)
                    continue

                raise EngineException("failed to classify exercise: " + exercise_name)

            else:
                print_verbose("N: User doesn't have the fixture(s) ({0}), skipping {1}".format(\
                   exercise.fixtures, exercise_name))
                self.unavailable_exercises.add(exercise_name)


    def set_user_routine_history(self, user_routine_history):
        """ set the user exercise history
        This should be a sequence of ExerciseSets
        """
        self.user_routine_history = user_routine_history

    def set_user_preferences(self, user_preferences):
        """ set the user preferences

        This describes general workout preferences which may or may not be used by the routines
        Used as a hint for some routines
        This should be a UserPreferences
        """
        self.user_preferences = user_preferences


    def generate_plan(self, generator, **kwargs):
        """ generates single plan by generator referred to by name with arbitrary args
        TODO document args in a consistent format
        This returns a sequence of ExerciseSets
        """

        if generator in self.generators:
            routine_environment = RoutineEnvironment(self.available_exercises,\
                self.unavailable_exercises, self.user_preferences, self.user_routine_history)
            return self.generators[generator].generate_plan(routine_environment, self.exercise_data, **kwargs)
        else:
            raise EngineException("Invalid generator: " + str(generator))
