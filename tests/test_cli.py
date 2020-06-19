#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dtw` package."""

import os.path

import unittest

from dtw.__main__ import *

here = os.path.dirname(os.path.abspath(__file__))

class TestCLI(unittest.TestCase):
    """Tests for `dtw` package."""

    def test_command_line_interface(self):
        """Test the CLI."""
        out = main2(os.path.join(here,"query.csv"),
                    os.path.join(here,"reference.csv"),
                    "symmetric2")
        assert '0.1292' in out

        
