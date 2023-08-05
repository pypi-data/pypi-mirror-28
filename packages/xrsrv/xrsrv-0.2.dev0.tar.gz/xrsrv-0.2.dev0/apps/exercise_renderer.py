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

""" Simple application for generating HTML routine """

import sys
import argparse
import json

from xrsrv import routine_engine
from xrsrv import exercise_rendering
from xrsrv import user_database
from xrsrv.routine_generators.generator_exception import GeneratorException


EXERCISE_DATABASE_NAME = "exercise.db"
USER_DATABASE_NAME = "user.db"

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-argument

def generate_and_render():
    """ Generates the list of exercises and renders the HTML """
    app_args_parser = argparse.ArgumentParser()
    app_args_parser.add_argument("--generator", type=str, help="generator to use", default="debug")
    app_args_parser.add_argument("--uid", type=str, help="database UID of user", required=True)
    app_args_parser.add_argument("--userdb", type=str, help="user db file name", default=USER_DATABASE_NAME)
    app_args_parser.add_argument("--exercisedb", type=str, help="exercise db file name",\
                                 default=EXERCISE_DATABASE_NAME)
    app_args_parser.add_argument("--json", help="JSON genrator arguments filename", required=False)
    app_args_parser.add_argument("--args", help="genrator arguments", nargs=argparse.REMAINDER)
    app_args = app_args_parser.parse_args()

    engine = routine_engine.RoutineEngine(app_args.exercisedb)

    user_db = user_database.Connection(app_args.userdb)
    user_fixtures = user_db.get_user_fixtures(app_args.uid)
    user_rigs = user_db.get_user_rigs(app_args.uid)

    json_args = {}
    if app_args.json is not None:
        with open(app_args.json) as f:
            json_args = json.load(f)

    # XXX this is cheesy.  Maybe add a subparser per generator?  Need to read from engine.
    generator_args = {}
    if app_args.args is not None:
        split_args = [arg.split("=") for arg in app_args.args]
        generator_args = {val[0]: val[1] for val in split_args}

    engine.set_user_exercise_environment(user_fixtures, user_rigs)
    plan = engine.generate_plan(app_args.generator, **{**generator_args, **json_args})

    basic_html_renderer = exercise_rendering.BasicHTMLRenderer()

    if plan:
        sys.stdout.write(basic_html_renderer.render("exercise_renderer output", plan))


if __name__ == "__main__":
    try:
        generate_and_render()
    except GeneratorException as ex:
        exit("Generator exception: {0}".format(ex))
    except routine_engine.EngineException as ex:
        exit("Engine exception: {0}".format(ex))
