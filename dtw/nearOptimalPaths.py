##
## Copyright (c) 2013-2026 of Toni Giorgino
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

"""List nearly-optimal warping paths"""

import numbers

import numpy

from dtw._dtw_utils import _nearOptimalPaths_search
from dtw.dtw import DTW

__all__ = ["nearOptimalPaths"]


def nearOptimalPaths(d, threshold=None, max_paths=10000):
    # IMPORT_RDOCSTRING nearOptimalPaths
    """List nearly-optimal warping paths

Enumerate all the warping paths whose cumulative distance does not
exceed a given threshold, i.e. the optimal alignment and its runners-up.

**Details**

[dtw()] returns one path of least cumulative distance. Other paths may
be equally good (ties) or only slightly worse. Listing them shows how
well determined the alignment is: parts of the warping curve shared by
all the nearly-optimal paths are robust, while parts where they spread
out are not.

The paths are found with the algorithm of Waterman and Byers (1985).
Paths are grown backwards from the end of the alignment. A partial path
is extended to a cell only if it can still be completed within
``threshold``. This is known from the cumulative cost matrix, which
holds the cost of the best path reaching each cell. No time is spent on
paths that are later discarded, so the run time is proportional to the
size of the output.

The problem parameters (local cost matrix, step pattern, window, open
end) are taken from ``d``, which must be computed with
``keep_internals=True``. The alignment found by [dtw()] is not used.

Open-end alignments are supported with ``"N"``-normalizable step
patterns (see [stepPattern()]), for which ranking paths by distance or
by normalized distance gives the same order. Paths may then end at any
column of the last row. Open-begin alignments are not supported.

Distances are compared with a small tolerance, proportional to the
rounding error expected when adding up a path (of the order of ``N+M``
times the machine epsilon, relative to ``threshold``). This ensures that
the default threshold returns all the optimal paths. The distance of the
path found by [dtw()] is identical to ``d.distance``.

The number of paths grows exponentially with the size of the problem
(see [countPaths()]), so thresholds far from the optimum can produce
very many paths, even for short timeseries. ``max_paths`` guards against
running out of memory.

Parameters
----------
d : 
    an object of class `dtw`, computed with `keep_internals=True`
threshold : 
    list paths whose cumulative distance (not normalized) is less than or equal to this value. The default (``None``) is ``d.distance``, which lists the optimal paths, including ties.
max_paths : 
    stop with an error if more than this many paths are within the threshold

Returns
-------

A list of paths, sorted by increasing distance. Each element is a `DTW`
object with the fields ``index1``, ``index2``, ``index1s``, ``index2s``, ``stepsTaken``,
``distance`` and ``normalizedDistance``, which have the same meaning as in [dtw()]
objects. The list is empty if ``threshold`` is below the optimal
distance. Otherwise, the first element is the path found by [dtw()], and
other paths with equal distance follow in an unspecified order.

References
----------

Michael S. Waterman, Thomas H. Byers. *A dynamic programming algorithm
to find all solutions in a neighborhood of the optimum.* Mathematical
Biosciences, 77(1-2), 179-188, 1985.
`doi:10.1016/0025-5564(85)90096-3 <https://doi.org/10.1016/0025-5564(85)90096-3>`__

Examples
--------
>>> from dtw import *
>>> import numpy as np

Compute the optimal alignment

>>> ds = dtw(np.arange(1, 8) + 2, np.arange(1, 9),
...          keep_internals=True, step_pattern=asymmetric)

There are 126 possible paths. List them all.

>>> allPaths = nearOptimalPaths(ds, threshold=np.inf)
>>> len(allPaths) == countPaths(ds)
True

How many paths have each distance

>>> np.unique([p.distance for p in allPaths], return_counts=True)[1]
array([ 1,  6, 10, 10, 11, 12, 13, 13, 12, 11,  9,  7,  5,  3,  2,  1])

The best path is the one found by dtw()

>>> np.array_equal(allPaths[0].index2, ds.index2)
True

Paths at most 1 unit worse than the optimum

>>> nearPaths = nearOptimalPaths(ds, threshold=ds.distance + 1)
>>> import matplotlib.pyplot as plt                 # doctest: +SKIP
>>> for p in nearPaths:                             # doctest: +SKIP
...     plt.plot(p.index1, p.index2, color="grey")
>>> plt.plot(ds.index1, ds.index2, color="red", lw=2)  # doctest: +SKIP
>>> plt.xlabel("Query index"); plt.ylabel("Reference index")  # doctest: +SKIP

"""
    # ENDIMPORT

    if not isinstance(d, DTW):
        raise TypeError("dtw object required")

    if not hasattr(d, "costMatrix") or not hasattr(d, "localCostMatrix"):
        raise ValueError("Cost matrices not available: call dtw() with keep_internals=True")

    if d.openBegin:
        raise ValueError("Open-begin alignments are not supported")

    norm = d.stepPattern.hint
    if d.openEnd and norm != "N":
        raise ValueError("Open-end alignments are only supported with N-normalizable step patterns")

    if threshold is None:
        threshold = d.distance
    if (not isinstance(threshold, numbers.Real) or isinstance(threshold, bool)
            or numpy.isnan(threshold)):
        raise ValueError("threshold should be a single number")
    threshold = float(threshold)

    if (not isinstance(max_paths, numbers.Real) or isinstance(max_paths, bool)
            or numpy.isnan(max_paths) or max_paths < 1):
        raise ValueError("max_paths should be a positive number")
    max_paths = int(min(max_paths, numpy.iinfo(numpy.intp).max))

    lm = numpy.ascontiguousarray(d.localCostMatrix, dtype=numpy.double)
    cm = numpy.ascontiguousarray(d.costMatrix, dtype=numpy.double)
    di, dj, sc, first = _unpackPattern(d.stepPattern.mx)

    n, m = cm.shape
    ends = numpy.arange(m) if d.openEnd else numpy.array([m - 1])

    # absorb rounding errors, which may differ along tied paths
    tol_threshold = threshold + (n + m) * len(sc) * numpy.finfo(float).eps * abs(threshold)

    raw = _nearOptimalPaths_search(lm, cm, di, dj, sc, first,
                                   numpy.ascontiguousarray(ends, dtype=numpy.intp),
                                   tol_threshold, max_paths)

    # the search sums costs backwards; check the forward sums too.
    # sorted() is stable, keeping the search order among ties
    raw = sorted((p for p in raw if p[5] <= tol_threshold), key=lambda p: p[5])

    return [_mkDTW(d, *p) for p in raw]


# Group the step pattern rows by pattern, keeping their order, and
# check that each pattern starts with its origin, as computeCM()
# assumes
def _unpackPattern(mx):
    mx = numpy.asarray(mx, dtype=numpy.double)
    if mx.ndim != 2 or mx.shape[0] == 0 or mx.shape[1] != 4:
        raise ValueError("Empty or malformed step pattern")

    pn = mx[:, 0]
    if numpy.any(pn != numpy.floor(pn)) or numpy.any(pn < 1) or \
            numpy.any(mx[:, 1:3] != numpy.floor(mx[:, 1:3])) or numpy.any(mx[:, 1:3] < 0):
        raise ValueError("Invalid step pattern")
    pn = pn.astype(numpy.intp) - 1
    npats = pn.max() + 1

    rows = numpy.argsort(pn, kind="stable")
    di = numpy.ascontiguousarray(mx[rows, 1], dtype=numpy.intp)
    dj = numpy.ascontiguousarray(mx[rows, 2], dtype=numpy.intp)
    sc = numpy.ascontiguousarray(mx[rows, 3], dtype=numpy.double)
    first = numpy.zeros(npats + 1, dtype=numpy.intp)
    first[1:] = numpy.cumsum(numpy.bincount(pn, minlength=npats))

    for k in range(npats):
        o = first[k]
        if first[k + 1] == o or sc[o] != -1.0 or di[o] + dj[o] == 0:
            raise ValueError("Pattern %d does not start with a valid origin" % (k + 1))
        if numpy.any(sc[o + 1:first[k + 1]] == -1.0):
            raise ValueError("Pattern %d has more than one origin" % (k + 1))

    return di, dj, sc, first


# Wrap a path in a DTW object, with the same normalizations as in dtw()
def _mkDTW(d, index1, index2, index1s, index2s, stepsTaken, distance):
    n = d.N
    jend = index2[-1] + 1
    norm = d.stepPattern.hint
    if norm == "N":
        nd = distance / n
    elif norm == "N+M":
        nd = distance / (n + jend)
    elif norm == "M":
        nd = distance / jend
    else:
        nd = numpy.nan

    return DTW({'index1': index1,
                'index2': index2,
                'index1s': index1s,
                'index2s': index2s,
                'stepsTaken': stepsTaken,
                'distance': distance,
                'normalizedDistance': nd,
                'N': d.N,
                'M': d.M,
                'jmin': index2[-1],
                'stepPattern': d.stepPattern,
                'openEnd': d.openEnd,
                'openBegin': d.openBegin})
