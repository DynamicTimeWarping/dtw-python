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
    #ENDIMPORT

    size = elasticity

    pn = numpy.repeat( numpy.arange(size)+1, 2)
    dx = numpy.tile( [1,0], size)
    dy = pn * dx
    w = numpy.tile( [-1,1], size)

    tmp = numpy.vstack([pn, dx, dy, w]).T

    return StepPattern(tmp,"N")

