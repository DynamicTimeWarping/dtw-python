
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
date. It is a faithful Python equivalent of `R's DTW package on CRAN
<https://cran.r-project.org/package=dtw>`__.  Supports arbitrary local (e.g.
symmetric, asymmetric, slope-limited) and global (windowing)
constraints, fast native code, several plot styles, and more.



Documentation
~~~~~~~~~~~~~

Please refer to the main `DTW project homepage
<https://dynamictimewarping.github.io>`__ for the full documentation
and background.

The best resource is a `companion
paper <http://www.jstatsoft.org/v31/i07/>`__, including detailed
instructions and extensive background on things like multivariate
matching, open-end variants for real-time use, interplay between
recursion types and length normalization, history, etc.

**Note**: **R** is the preferred environment for the DTW
project. Python's docstrings and the API below are generated
automatically for the sake of consistency and maintainability, and may
not be as pretty.


Citation
~~~~~~~~

When using in academic works please cite:

* T. Giorgino. Computing and Visualizing Dynamic Time Warping Alignments in R: The dtw Package. J. Stat. Soft., 31 (2009) `doi:10.18637/jss.v031.i07 <https://www.jstatsoft.org/article/view/v031i07>`__.

When using partial matching (unconstrained endpoints via the open.begin/open.end options) and/or normalization strategies, please also cite:

* P. Tormene, T. Giorgino, S. Quaglini, M. Stefanelli (2008). Matching Incomplete Time Series with Dynamic Time Warping: An Algorithm and an Application to Post-Stroke Rehabilitation. Artificial Intelligence in Medicine, 45(1), 11-34. `doi:10.1016/j.artmed.2008.11.007 <http://dx.doi.org/10.1016/j.artmed.2008.11.007>`__

  
License
~~~~~~~

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.




API
===

.. automodapi:: dtw
		
