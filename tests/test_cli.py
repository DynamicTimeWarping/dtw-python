#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `dtwr` package."""


import unittest

from dtwr import cli


class TestCLI(unittest.TestCase):
    """Tests for `dtwr` package."""

    def test_command_line_interface(self):
        """Test the CLI."""
        out = cli.main("tests/query.csv","tests/reference.csv","symmetric2")
        assert '0.1292' in out

        
