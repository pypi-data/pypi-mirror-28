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

""" The type factories generating the abstractions of data in the database """

import collections

# **** Exercise types ****
# Muscle: The details of a muscle
# name: muscle name
# group: muscle grouping
# antagonists: muscle antagonists
# info: dictionary of additional information about the muscle
Muscle = collections.namedtuple("Muscle", "name, group, antagonist, info")

# Exercise: The details of an exercise
# name: exercise name
# fixtures: fixtures required
# rigs: rigs to be used with this exercise
# muscles_exercised: list of muscles exercised
# info: dictionary of additional information about the exercise
Exercise = collections.namedtuple(\
    "Exercise", "name, fixtures, rigs, muscles_exercised, info")

# ExerciseRig: A generic set of non-fixed equipment required or optional for given exercise
# name: rig name
# optional: optional in exercise
ExerciseRig = collections.namedtuple("ExerciseRig", "name, optional")

# ExerciseSet: An instance of an exercise whether in the past or future
# exercise_name: exercise name
# duration: number of repetitions done or seconds exercising
# setting: setting at which to do the reps
# time: time when exercise was completed or is to be completed or None if N/A
ExerciseSet = collections.namedtuple("ExerciseSet", "name, duration, setting, time")

# RoutineEnvironment: The overall representation of the user to the routine engine
# available_exercises: set of available exercise names
# unavailable_exercises: set of unavailable exercise names
# exercise_set_history: exercise set history directly preceding generation
# user_preferences: user preferences
RoutineEnvironment = collections.namedtuple(\
    "RoutineEnvironment", "available_exercises, unavailable_exercises, exercise_set_history, user_preferences")


# **** User types ****
# UserProfile general information about a user
# uid: the unique id for the user
# name: user's actual name
# notes: a placeholder for additional information
UserProfile = collections.namedtuple("UserProfile", "uid, name, notes")

# UserFixture: A fixture with optional max and min settings
# name: fixture name
# min_setting: either minimum speed, weight, or resistance
# max_setting: either maximum speed, weight, or resistance
UserFixture = collections.namedtuple("UserFixture", "name, min_setting, max_setting")

# UserRig: A rig with possible resistance settings based on EquipmentAccessories on hand
# name: rig name
# min_setting: either minimum speed, weight, or resistance
# max_setting: either maximum speed, weight, or resistance
UserRig = collections.namedtuple("UserRig", "name, min_setting, max_setting")

# UserPreference: The set of values used by any or all of the routine generators
# this differs from the values specific to each type of routine passed to the generate function
# name: rig name
# muscles_to_target: a set of muscles the user would like to target
# muscles_to_avoid: a set of muscles the user would like to avoid due to injury, etc.
# preferred_exrcises: a set of exercises the user would like to be included in a routine
# eschewed_exrcises: a set of exercises the user would like to not be included in a routine
UserPreferences = collections.namedtuple(\
    "UserPreferences", "muscles_to_target, muscles_to_avoid, preferred_exercises, eschewed_exercises")
