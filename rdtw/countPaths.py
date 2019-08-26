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

    
