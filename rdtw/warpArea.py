import numpy
from scipy.interpolate import interp1d

def warpArea(d):

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

