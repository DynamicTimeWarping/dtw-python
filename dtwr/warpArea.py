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
from scipy.interpolate import interp1d

def warpArea(d):
    #IMPORT_RDOCSTRING warpArea
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





"""
    #ENDIMPORT

    # interp1d is buggy. it does not deal with duplicated values of x
    # leading. it returns different values depending on the dtypes of
    # arguments.
    ifun = interp1d(x=d.index1, y=d.index2 )
    ii = ifun(numpy.arange(d.N))

    # Kludge
    ii[numpy.isnan(ii)] = d.index2[0]

    dg = np.linspace(0, d.M-1, num=d.N-1)

    ad = numpy.abs(ii-dg)
    return numpy.sum(ad)

