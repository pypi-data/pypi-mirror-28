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

""" HTML rendering classes """

import abc
import textwrap

# pylint: disable=too-few-public-methods
# pylint: disable=no-self-use
# pylint: disable=unused-argument
# pylint: disable=no-member

class BaseRenderer(metaclass=abc.ABCMeta):
    """ Abstract base class for rendering classes """

    def render(self, exercise_data):
        """ Render the exercise data
        TODO this only handles a single set of data; needs to be more powerful (PoC)
        """
        return ""

class BasicHTMLRenderer(object):
    """ Renderer that creates a VERY basic html table of data """

    def render(self, title, exercise_data):
        """ Render the excercise data in HTML

        This is a simple table for printing onto paper (not meant to be pretty)
        """

        if len(exercise_data) == 1:
            body = "    <table>\n"
            body += "    <tr><th>Exercise</th><th>Muscles</th><th>Fixture(s)</th>"\
                "<th>Rig(s)</th></tr>\n"
            this_exercise_data = exercise_data[0]
            for exercise in this_exercise_data:
                if exercise.rigs is not None:
                    rig_names = ", ".join(["({0})".format(rig.name) if rig.optional else rig.name for rig in exercise.rigs])
                else:
                    rig_names = ""
                body += "{0}<tr><td>{1}</td><td>{2}</td><td>{3}</td>"\
                    "<td>{4}</td></tr>\n".format(\
                        " " * 16, exercise.name, ", ".join(exercise.muscles_exercised),\
                        ", ".join(exercise.fixtures), rig_names)
            body += "    </table>\n"

            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{0}</title>
                <style>
                    table {{
                        border-collapse: collapse;
                    }}
                    table, th, td {{
                        border: 1px solid black;
                    }}
                </style>
            </head>
            <body>
            {1}
            </body>
            </html>
            """.format(title, body)
        else:
            body = "    <table>\n    "
            
            NUM_SETS_PER_EXERCISE = 3
            for day_i, day in enumerate(exercise_data):
                body += "<tr><td class=\"heady\">Day {0}</td>".format(day_i + 1)
                for exercise in day:
                    body += "<td><table class=\"checkly\">{1}</table>{0}</td>".format(exercise.name, "<td></td>"\
                        * NUM_SETS_PER_EXERCISE)
                body += "</tr>\n"

            body += "    </table>"
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{0}</title>
                <style>
                    table {{
                        border-collapse: collapse;
                        font-family: "Courier New", sans-serif;
                        table-layout: fixed;
                        font-size: 60%;
                    }}
                    table.checkly {{
                    }}
                    table.checkly td {{
                        width: 13px;
                        height: 13px;
                    }}
                    td {{
                        overflow: hidden;
                        width: 100px;
                    }}
                    td.heady {{
                        background-color: black;
                        color: white;
                    }}
                    table, th, td {{
                        border: 1px solid black;
                        text-align: left;
                        vertical-align: top;
                    }}
                </style>
            </head>
            <body>
            {1}
            </body>
            </html>
            """.format(title, body)

        return textwrap.dedent(html)

BaseRenderer.register(BasicHTMLRenderer)
