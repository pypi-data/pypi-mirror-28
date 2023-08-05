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

""" Very basic routine generation """
import random
from xrsrv.routine_generators.generator_exception import GeneratorException

def generate_plan(routine_environment, exercise_data, **kwargs):
    """ generates single plan
    This is a quick and dirty first pass with limited functionality and a crude
    selection algorithm
    TODO document args in a consistent format
    returns a list of one list of exercises
    """

    if len(routine_environment.available_exercises) == 0:
        raise GeneratorException("No available exercises from which to choose")

    if 'n' not in kwargs:
        raise GeneratorException("Missing argument n")

    try:
        choose_n = int(kwargs['n'])
    except Exception as ex:
        raise GeneratorException("Failed to convert n argument: {0}".format(ex))

    exercise_names = random.sample(routine_environment.available_exercises,\
        min(choose_n, len(routine_environment.available_exercises)))
    return [[exercise_data[name] for name in exercise_names]]
