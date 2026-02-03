
import unittest

import numpy as np
import matplotlib

matplotlib.use("Agg")

from dtw import *

""" 
From the "quickstart" examples.
"""

class TestPlot(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        # A noisy sine wave as query
        self.idx = np.linspace(0, 6.28, num=100)
        self.query = np.sin(self.idx) + np.random.uniform(size=100) / 10.0

        # A cosine is for template; sin and cos are offset by 25 samples
        self.template = np.cos(self.idx)

    def test_plot_threeway(self):
        """Test the three-way plot."""
        # Find the best match with the canonical recursion formula
        alignment = dtw(self.query, self.template, keep_internals=True)

        # Display the warping curve, i.e. the alignment curve
        alignment.plot(type="threeway")

    def test_plot_twoway(self):
        """Test the two-way plot."""
        # Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
        dtw(
            self.query,
            self.template,
            keep_internals=True,
            step_pattern=rabinerJuangStepPattern(6, "c"),
        ).plot(type="twoway", offset=-2)

    def test_plot_step_pattern(self):
        """Test the step pattern plot."""
        # See the recursion relation, as formula and diagram
        print(rabinerJuangStepPattern(6, "c"))
        rabinerJuangStepPattern(6, "c").plot()
