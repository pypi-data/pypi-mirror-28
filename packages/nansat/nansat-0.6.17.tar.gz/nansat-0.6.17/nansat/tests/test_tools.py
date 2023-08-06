#------------------------------------------------------------------------------
# Name:         test_nansat.py
# Purpose:      Test the Nansat class
#
# Author:       Morten Wergeland Hansen, Asuka Yamakawa
# Modified: Morten Wergeland Hansen
#
# Created:      18.06.2014
# Last modified:16.04.2015 10:48
# Copyright:    (c) NERSC
# Licence:      This file is part of NANSAT. You can redistribute it or modify
#               under the terms of GNU General Public License, v.3
#               http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------------------------
import unittest
import datetime

from matplotlib.colors import hex2color
from nansat.tools import get_random_color, parse_time

class ToolsTest(unittest.TestCase):
    def test_get_random_color(self):
        ''' Should return HEX code of random color '''
        c0 = get_random_color()
        c1 = get_random_color(c0)
        c2 = get_random_color(c1, 300)

        self.assertEqual(type(hex2color(c0)), tuple)
        self.assertEqual(type(hex2color(c1)), tuple)
        self.assertEqual(type(hex2color(c2)), tuple)

    def test_parse_time(self):
        dt = parse_time('2016-01-19')

        self.assertEqual(type(dt), datetime.datetime)

    def test_parse_time_incorrect(self):
        dt = parse_time('2016-01-19Z')

        self.assertEqual(type(dt), datetime.datetime)
