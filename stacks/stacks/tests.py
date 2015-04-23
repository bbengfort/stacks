# stacks.tests
# Tests for the Stacks project module
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Wed Apr 22 20:05:44 2015 -0400
#
# Copyright (C) 2015 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: tests.py [] benjamin@bengfort.com $

"""
Tests for the Stacks project module
"""

##########################################################################
## Imports
##########################################################################

import os
import unittest

##########################################################################
## Initialization Tests
##########################################################################

EXPECTED_VERSION = "0.2"


class InitializationTests(unittest.TestCase):

    def test_sanity(self):
        """
        Check the world is sane and 2+2=4
        """

        self.assertEqual(2 + 2, 4)

    def test_import(self):
        """
        Ensure we can import the elmr module
        """

        try:
            import stacks
        except ImportError:
            self.fail("Could not import the stacks module")

    def test_version(self):
        """
        Check that the test version matches the ELMR version
        """

        import stacks
        self.assertEqual(stacks.__version__, EXPECTED_VERSION)

    def test_testing_mode(self):
        """
        Assert that we are in testing mode
        """
        self.assertEqual(os.environ["DJANGO_SETTINGS_MODULE"], "stacks.settings.testing")
