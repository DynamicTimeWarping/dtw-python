##
## Copyright (c) 2006-2026 of Toni Giorgino
##
## This file is part of the DTW package.
##
## DTW is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## DTW is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.
##
## You should have received a copy of the GNU General Public License
## along with DTW.  If not, see <http://www.gnu.org/licenses/>.
##

"""Compute a dissimilarity matrix"""

import numpy

from dtw.dtw import dtw

__all__ = ["dtwDist"]


def dtwDist(mx, my=None, **kwargs):
    """Compute a dissimilarity matrix

Compute the dissimilarity matrix between a set of single-variate
timeseries.

**Details**

``dtwDist`` computes a dissimilarity matrix, akin to
``scipy.spatial.distance.cdist``, based on the Dynamic Time Warping
definition of a distance between single-variate timeseries.

The timeseries are stored as rows in the matrix argument ``mx``. In
other words, if ``mx`` is an N \\* T matrix, ``dtwDist`` will build N \\*
N ordered pairs of timeseries, perform the corresponding N \\* N
[dtw()] alignments, and return all of the results in a matrix. Each of
the timeseries is T elements long. Timeseries of different lengths can
be passed as a list of 1-D arrays instead.

``dtwDist`` returns a square matrix, rather than the condensed form
returned by ``scipy.spatial.distance.pdist``. This makes sense because
in general the DTW “distance” is not symmetric (see e.g. asymmetric
step patterns).

Parameters
----------
mx :
    numeric matrix, containing timeseries as rows, or a list of 1-D arrays
my :
    numeric matrix, containing timeseries as rows, or a list of 1-D arrays (for cross-distance). Defaults to ``mx``.
**kwargs :
    arguments passed to the [dtw()] call

Returns
-------

A matrix whose element ``[i,j]`` holds the Dynamic Time Warp distance
between row ``i`` (query) of ``mx`` and row ``j`` (reference) of
``my``, i.e. ``dtw(mx[i], my[j]).distance``. Its shape is
``(len(mx), len(my))``.

Notes
-----

To convert a square dissimilarity matrix to the condensed form used by
``scipy.cluster.hierarchy``, use a suitable symmetrization strategy (see
examples) and then ``scipy.spatial.distance.squareform``.

Examples
--------
>>> from dtw import *
>>> import numpy as np

Symmetric step pattern => symmetric dissimilarity matrix

>>> m = np.tile(np.arange(1, 5), (3, 1)).T
>>> dtwDist(m)
array([[ 0.,  5., 10., 15.],
       [ 5.,  0.,  5., 10.],
       [10.,  5.,  0.,  5.],
       [15., 10.,  5.,  0.]])

Find the optimal warping _and_ scale factor at the same time.
(There may be a better, analytic way)

Prepare a query and a reference

>>> query = np.sin(np.linspace(0, 4 * np.pi, 100))
>>> reference = np.cos(np.linspace(0, 4 * np.pi, 100))

Make a set of several references, scaled from 0 to 3 in .1 increments.
Put them in a matrix, in rows

>>> scaleSet = np.arange(1, 31) / 10
>>> referenceSet = np.outer(1 / scaleSet, reference)

The query has to be made into a 1-row matrix.
Perform all of the alignments at once, and normalize the result.

>>> distanceSet = dtwDist(query[np.newaxis, :], referenceSet)[0]

The optimal scale for the reference is close to 1.0

>>> scaleSet[np.argmin(scaleSet * distanceSet)]
np.float64(1.1)

>>> import matplotlib.pyplot as plt                       # doctest: +SKIP
>>> plt.plot(scaleSet, scaleSet * distanceSet, "o-")      # doctest: +SKIP

Asymmetric step pattern: we can either disregard part of the pairs,
or average with the transpose

>>> mm = np.random.default_rng(1).uniform(size=(4, 3))
>>> dm = dtwDist(mm, step_pattern=asymmetric)

Symmetrize by averaging:

>>> dms = (dm + dm.T) / 2

Check definition

>>> bool(dm[1, 0] == dtw(mm[1, :], mm[0, :], step_pattern=asymmetric).distance)
True

"""

    if my is None:
        my = mx
    mx = _asSeriesList(mx)
    my = _asSeriesList(my)

    out = numpy.empty((len(mx), len(my)))
    for i, x in enumerate(mx):
        for j, y in enumerate(my):
            out[i, j] = dtw(x, y, distance_only=True, **kwargs).distance
    return out


# Rows of a matrix, or a list of single-variate timeseries
def _asSeriesList(m):
    if isinstance(m, numpy.ndarray):
        if m.ndim == 1:
            m = m[numpy.newaxis, :]
        if m.ndim != 2:
            raise ValueError("A matrix of timeseries, stored as rows, was expected")
        return list(m)
    out = [numpy.asarray(x) for x in m]
    for x in out:
        if x.ndim != 1:
            raise ValueError("Timeseries should be 1-D arrays")
    return out
