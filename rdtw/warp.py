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
