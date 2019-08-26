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


def warp(d, index_reference=False):
    if not index_reference:
        iset = d.index1
        jset = d.index2
    else:
        iset = d.index2,
        jset = d.index1

    jmax = numpy.max(jset)

    # interp1d is buggy. it does not deal with duplicated values of x
    # leading. it returns different values depending on the dtypes of
    # arguments.
    ifun = interp1d(x=jset, y=iset )
    ii = ifun(numpy.arange(jmax))

    # Quick fix for bug
    ii[numpy.isnan(ii)] = iset[0]
    return ii
