
Welcome to the dtw-python package
=================================

Comprehensive implementation of `Dynamic Time Warping algorithms
<https://dynamictimewarping.github.io>`__.

DTW is a family of algorithms which compute the local stretch or
compression to apply to the time axes of two timeseries in order to
optimally map one (query) onto the other (reference). DTW outputs the
remaining cumulative distance between the two and, if desired, the
mapping itself (warping function). DTW is widely used e.g. for
classification and clustering tasks in econometrics, chemometrics and
general timeseries mining.

This package provides the most complete, freely-available (GPL)
implementation of Dynamic Time Warping-type (DTW) algorithms up to
date. It is a faithful Python equivalent of `R's DTW package
<http://dtw.r-forge.r-project.org/>`__.  Supports arbitrary local (eg
symmetric, asymmetric, slope-limited) and global (windowing)
constraints, fast native code, several plot styles, and more.



Documentation
~~~~~~~~~~~~~

Please refer to the main `DTW project homepage
<https://dynamictimewarping.github.io>`__ for the full documentation
and background.

The package is described in a `companion
paper <http://www.jstatsoft.org/v31/i07/>`__, including detailed
instructions and extensive background on things like multivariate
matching, open-end variants for real-time use, interplay between
recursion types and length normalization, history, etc.

**Note**: **R** is the preferred environment for the DTW project. The
documentation below is generated from that of `R's DTW package
<http://dtw.r-forge.r-project.org/>`__.


API
===

.. automodapi:: dtw
		
