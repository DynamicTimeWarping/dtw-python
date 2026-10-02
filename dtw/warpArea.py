##
## Copyright (c) 2006-2019 of Toni Giorgino
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

"""Warping path area computation"""

import numpy
from dtw.warp import _interp


def warpArea(d):
    # IMPORT_RDOCSTRING warpArea
    """Compute Warping Path Area

Compute the area between the warping function and the diagonal
(no-warping) path, in unit steps.

**Details**

Above- and below- diagonal unit areas all count *plus* one (they do not
cancel with each other). The “diagonal” goes from one corner to the
other of the possibly rectangular cost matrix, therefore having a slope
of ``M/N``, not 1, as in [slantedBandWindow()].

The computation is approximate: points having multiple correspondences
are averaged, and points without a match are interpolated. Therefore,
the area can be fractionary.

Parameters
----------
d : 
    an object of class `dtw`

Returns
-------

The area, not normalized by path length or else.

Notes
-----

There could be alternative definitions to the area, including
considering the envelope of the path.

Examples
--------
>>> from dtw import *

>>> ds = dtw( [1,2,3,4], [1,2,3,4,5,6,7,8]);

>>> import matplotlib.pyplot as plt;
... ds.plot(); plt.plot([0,2.3,4.7,7])		# doctest: +SKIP

>>> float(warpArea(ds))
6.0

>>> ## Result: 6
>>> ##  index 2 is 2 while diag is 3_3  (+1_3)
>>> ##        3    3               5_7  (+2_7)
>>> ##        4   4:8 (avg to 6)    8   (+2  )
>>> ##                                 --------
>>> ##                                     6

"""
    # ENDIMPORT

    ifun = _interp(x=d.index1, y=d.index2)
    ii = ifun(numpy.arange(d.N))

    dg = numpy.linspace(0, d.M - 1, num=d.N)

    ad = numpy.abs(ii - dg)
    return numpy.sum(ad)
