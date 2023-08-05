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

""" Test cases for classes in exercise_rendering.py """

import unittest

from xrsrv import routine_engine
from xrsrv import exercise_rendering

EXERCISE_DATABASE_NAME = "exercise.db"

class TestExerciseHTMLRendering(unittest.TestCase):
    """
    Test the exercise HTML rendring classes

    TODO(jessepinnell) refactor or make these more robust tests
    """

    def __init__(self, *args, **kwargs):
        super(TestExerciseHTMLRendering, self).__init__(*args, **kwargs)
        self.engine = routine_engine.RoutineEngine(EXERCISE_DATABASE_NAME)
        self.basic_html_renderer = exercise_rendering.BasicHTMLRenderer()

    def test_instantiation(self):
        """ Test the creation of the connection to the database """
        self.assertIsInstance(self.basic_html_renderer, exercise_rendering.BasicHTMLRenderer)


    def test_basic_html_renderer(self):
        """ Test the basic_html_renderer.render() method """
        num_exercises_in_plan = 14
        self.engine.set_user_exercise_environment([], [])
        plan = self.engine.generate_plan("basic_random", n=num_exercises_in_plan)
        self.assertEqual(len(plan), num_exercises_in_plan)

        # TODO perform HTML validation as test
        # lxml would work, but it would add requirement to project just for this
        self.assertNotEqual(len(self.basic_html_renderer.render("", plan)), 0)


if __name__ == '__main__':
    unittest.main()
