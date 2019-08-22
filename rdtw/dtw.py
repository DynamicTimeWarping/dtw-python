# Author: Toni Giorgino 2018
#
# If you use this software in academic work, please cite:
#  * T. Giorgino. Computing and Visualizing Dynamic Time Warping
#    Alignments in R: The dtw Package. Journal of Statistical
#    Software, v. 31, Issue 7, p. 1 - 24, aug. 2009. ISSN
#    1548-7660. doi:10.18637/jss.v031.i07. http://www.jstatsoft.org/v31/i07/


from __future__ import division, print_function, absolute_import

import numpy as np
from ._dtw_utils import *
from scipy.spatial.distance import cdist

__all__ = ['dtw',
           'symmetric1', 'symmetric2', 'asymmetric']


# --------------------

class StepPattern:
    def __init__(self, mx, hint):
        self.mx = np.array(mx, dtype=np.double)
        self.hint = hint

    def get_p(self):
        # Dimensions are reversed wrt R
        s = self.mx[:, [0, 2, 1, 3]]
        return s.T.reshape(-1)

    def get_n_rows(self):
        return self.mx.shape[0]

    def get_n_patterns(self):
        return int(np.max(self.mx[:,0]))


# TODO: all step patterns and generation functions
symmetric2 = StepPattern(np.array([[1, 1, 1, -1, ],
                                   [1, 0, 0, 2, ],
                                   [2, 0, 1, -1, ],
                                   [2, 0, 0, 1, ],
                                   [3, 1, 0, -1, ],
                                   [3, 0, 0, 1]]),
                         "N+M")

symmetric1 = StepPattern(np.array([[1, 1, 1, -1, ],
                                   [1, 0, 0, 1, ],
                                   [2, 0, 1, -1, ],
                                   [2, 0, 0, 1, ],
                                   [3, 1, 0, -1, ],
                                   [3, 0, 0, 1]]),
                         "NA")

asymmetric = StepPattern(np.array([[1, 1, 0, -1],
                                   [1, 0, 0, 1],
                                   [2, 1, 1, -1],
                                   [2, 0, 0, 1],
                                   [3, 1, 2, -1],
                                   [3, 0, 0, 1]]),
                         "N")


# --------------------

class DTW:
    def __init__(self, obj):
        self.__dict__.update(obj)

    def __repr__(self):
        s = "DTW alignment object of size (query x reference): {:d} x {:d}".format(self.N, self.M)
        return (s)


# --------------------


def dtw(x, y=None,
        dist_method="euclidean",
        step_pattern=symmetric2,
        window_type=None,
        keep_internals=False,
        distance_only=False,
        open_end=False,
        open_begin=False):
    """Compute Dynamic Time Warp and find optimal alignment between two time series.

    Under development. The syntax mirrors the one in R 'dtw' package
    (please see links below), except that dots in argument names are
    replaced by underscores.

    Parameters
    ----------

    x : array_like
       First input. A timeseries (1D or higher dimension), with time in rows.
       If y = None, interpreted as the local distance matrix instead.
    y : array_like
       Second input. A timeseries (1D or higher dimension), with time in rows.
    dist_method : str, optional
       One of the distance metrics supported by scipy.spatial.distance.cdist
       Defaults to 'euclidean'
    step_pattern : object, optional
       An object representing the recursion form, i.e. local slope constraints.
       Currenly only symmetric1 and symmetric2 are implemented.
    distance_only : bool, optional
       Only compute the distance, not the alignment (may be slightly faster
       and memory-efficient)


    Returns
    -------
    alignment : object
        an instance of type DTW encapsulating the same properties as the R implementation (q.v.),
        and in particular see:
            .distance
            .costMatrix
            .index1 etc.

    See also
    --------
     * https://cran.r-project.org/web/packages/dtw/index.html
     * http://dtw.r-forge.r-project.org
     * https://www.rdocumentation.org/packages/dtw/versions/1.20-1/topics/dtw

    Citation
    --------
    If you use this software in academic work, please cite:

     * T. Giorgino. Computing and Visualizing Dynamic Time Warping
       Alignments in R: The dtw Package. Journal of Statistical
       Software, v. 31, Issue 7, p. 1 - 24, aug. 2009. ISSN
       1548-7660. doi:10.18637/jss.v031.i07. http://www.jstatsoft.org/v31/i07/

    Examples
    --------
    The worked-out exercise in section 3.9 of http://www.jstatsoft.org/v31/i07/ and
    Rabiner-Juang's book (Exercise 4.7 page 226).

    >>> from scipy.signal.dtw import *
    >>> lm = np.array( [[ 1,1,2,2,3,3 ],
                        [ 1,1,1,2,2,2 ],
                        [ 3,1,2,2,3,3 ],
                        [ 3,1,2,1,1,2 ],
                        [ 3,2,1,2,1,2 ],
                        [ 3,3,3,2,1,2 ]], dtype=np.double)
    >>> alignment = dtw(lm, step_pattern=asymmetric)
    >>> alignment.costMatrix

    """

    if open_end or open_begin or window_type:
        raise ValueError("Only the basic DTW functionality is implemented in scipy. Please use the R version.")

    if y is None:
        x = np.array(x)
        if len(x.shape) != 2:
            raise ValueError("A 2D local distance matrix was expected")
        lm = np.array(x)
    else:
        x = np.atleast_2d(x)
        y = np.atleast_2d(y)
        if x.shape[0] == 1:
            x = x.T
        if y.shape[0] == 1:
            y = y.T
        lm = cdist(x, y, metric=dist_method)

    n, m = lm.shape

    w = np.ones_like(lm, dtype=np.int32)

    sp = np.array(step_pattern.get_p(), dtype=np.double)

    nsp = np.array([step_pattern.get_n_rows()], dtype=np.int32)

    cm = np.full_like(lm, np.nan, dtype=np.double)
    cm[0, 0] = lm[0, 0]

    ncm, sm = _computeCM(w,
                         lm,
                         nsp,
                         sp,
                         cm)

    dist = ncm[n - 1, m - 1]

    jmin = m - 1

    if dist != dist:  # nan
        raise ValueError("No warping path found compatible with the local constraints")

    if step_pattern.hint == "N+M":
        ndist = dist/(n+m)
    elif step_pattern.hint == "N":
        ndist = dist/n
    elif step_pattern.hint == "M":
        ndist = dist/m
    else:
        ndist = np.nan
    
    out = {
        'N': n,
        'M': m,
        'jmin': jmin,
        'distance': dist,
        'normalizedDistance': ndist,
        'costMatrix': ncm,
        'directionMatrix': sm,
        'localCostMatrix': lm,
        'stepPattern': step_pattern,
    }

    dout = DTW(out)
    
    if not distance_only:
        bt = _backtrack(dout)
        dout.__dict__.update(bt)

    return dout



# ----------------------------------------

# This is O(n). Let's not make it unreadable.
def _backtrack(al):
    n = al.N
    m = al.M
    i = n-1
    j = al.jmin

    iis=[i]; ii=[i];
    jjs=[j]; jj=[j];
    ss=[]

    # Drop null deltas
    dir = al.stepPattern.mx
    dir = dir[ np.bitwise_or( dir[:,1] != 0,
                              dir[:,2] != 0), : ]

    # Split by 1st column
    npat = al.stepPattern.get_n_patterns()
    stepsCache = dict()
    for q in range(1,npat+1):
        tmp = dir[ dir[:,0] == q, ]
        stepsCache[q] = np.array(tmp[:,[1,2]],
                                 dtype=np.int)
        

    while True:
        if i==0 and j==0: break

        # Direction taken, 1-based
        s = al.directionMatrix[i,j]

        if s != s: break        # nan

        # undo the steps
        ss.insert(0,s)
        steps = stepsCache[s]

        ns = steps.shape[0]
        for k in range(ns):
            ii.insert(0, i-steps[k,0])
            jj.insert(0, j-steps[k,1])

        i -= steps[k,0]
        j -= steps[k,1]

        iis.insert(0,i)
        jjs.insert(0,j)

    out = { 'index1': ii,
            'index2': jj,
            'index1s': iis,
            'index2s': jjs,
            'stepsTaken': ss }

    return(out)


# ----------------------------------------


print("Importing the dtw module. When using in academic works please cite:\n T. Giorgino. Computing and Visualizing Dynamic Time Warping Alignments in R: The dtw Package.\n J. Stat. Soft., doi:10.18637/jss.v031.i07.\n")

