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




from .dtw import DTW
import numpy


def countPaths(d, debug=False):
    N = d.N
    M = d.M
    m = numpy.full((N,M), numpy.nan)

    if d.openBegin:
        m[0,:] = 1.0
    else:
        m[0,0] = 1.0

    dir = d.stepPattern
    npats = dir.get_n_patterns()
    # nsteps = dir.get_n_rows()
    deltas = dir._mkDirDeltas()

    wf = d.windowFunction

    for ii in range(N):
        for jj in range(M):
            if numpy.isfinite(m[ii,jj]):
                continue

            if not wf(ii, jj,
                      query_size = N,
                      reference_size = M,
                      **d.windowArgs):
                m[ii,jj] = 0
                continue

            np = 0
            for k in range(npats):
                ni = ii - deltas[k,0]
                nj = jj - deltas[k,1]

                if ni>=0 and nj>=0:
                    np += m[ni,nj]

            m[ii,jj] = np
              
    if debug:
        return m

    if d.openEnd:
        return numpy.sum(m[-1,])
    else:
        return m[-1,-1]

    
