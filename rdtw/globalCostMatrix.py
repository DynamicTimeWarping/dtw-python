import numpy
from .window import noWindow
from ._dtw_utils import _computeCM_wrapper


def _globalCostMatrix(lm,
                      step_pattern,
                      window_function,
                      seed=None):

    n, m = lm.shape
     
    nsteps = numpy.array([step_pattern.get_n_rows()], dtype=numpy.int32)

    if seed is not None:
        cm = seed
    else:
        cm = numpy.full_like(lm, numpy.nan, dtype=numpy.double)
        cm[0, 0] = lm[0, 0]

    sm = numpy.full_like(lm, numpy.nan, dtype=numpy.double)

    wm = numpy.full_like(lm, True, dtype=numpy.int32)
    if window_function != noWindow: # for performance
        for i in range(n):
            for j in range(m):
                wm[i,j] = window_function(i, j, query_size=n, reference_size=m)


    dir = step_pattern.get_p()

                
    # All input arguments
    out = _computeCM_wrapper(wm,
                             lm,
                             nsteps,
                             dir,
                             cm)

    out['stepPattern'] = step_pattern;
    return out

