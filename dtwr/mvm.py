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



import numpy
from .stepPattern import *

def mvmStepPattern(elasticity=20):
    #IMPORT_RDOCSTRING mvmStepPattern
    """Minimum Variance Matching algorithm


Step patterns to compute the Minimum Variance Matching (MVM)
correspondence between time series


**Details**

The Minimum Variance Matching algorithm (1) finds the non-contiguous
parts of reference which best match the query, allowing for arbitrarily
long “stretches” of reference to be excluded from the match. All
elements of the query have to be matched. First and last elements of the
query are anchored at the boundaries of the reference.

The ``mvmStepPattern`` function creates a ``stepPattern`` object which
implements this behavior, to be used with the usual [dtw()] call (see
example). MVM is computed as a special case of DTW, with a very large,
asymmetric-like step pattern.

The ``elasticity`` argument limits the maximum run length of reference
which can be skipped at once. If no limit is desired, set ``elasticity``
to an integer at least as large as the reference (computation time grows
linearly).



Parameters
----------

elasticity : 
    integer: maximum consecutive reference elements skippable


Returns
-------

A step pattern object.



Notes
-----

(None)




"""
    #ENDIMPORT

    size = elasticity

    pn = numpy.repeat( numpy.arange(size)+1, 2)
    dx = numpy.tile( [1,0], size)
    dy = pn * dx
    w = numpy.tile( [-1,1], size)

    tmp = numpy.vstack([pn, dx, dy, w]).T

    return StepPattern(tmp,"N")

