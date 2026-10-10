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

# cython: language_level=3, freethreading_compatible=True

"""Utility functions for DTW alignments."""

# Author: Toni Giorgino 2018
#
# If you use this software in academic work, please cite:
#  * T. Giorgino. Computing and Visualizing Dynamic Time Warping
#    Alignments in R: The dtw Package. Journal of Statistical
#    Software, v. 31, Issue 7, p. 1 - 24, aug. 2009. ISSN
#    1548-7660. doi:10.18637/jss.v031.i07. http://www.jstatsoft.org/v31/i07/


import numpy as np

# from cpython cimport array

from cpython.exc cimport PyErr_CheckSignals
from libc.math cimport isfinite

__all__ = ["_computeCM_wrapper", "_nearOptimalPaths_search"]

cdef extern from "dtw_core.h":
  void computeCM(			
	       const int *s,		
	       const int *wm,		
	       const double *lm,	
	       const int *nstepsp,	
	       const double *dir,	
	       double *cm,      # IN+OUT
	       int *sm          # OUT
  ) noexcept nogil




  
def _computeCM_wrapper(int [:,::1] wm not None,
                       double [:,::1] lm not None,
                       int [:] nstepsp not None,
                       double [::1] dir not None,
                       double [:,::1] cm not None,
                       int [:,::1] sm = None  ):

    # computeCM trusts its inputs: check them here, where we can raise.
    if not (wm.shape[0] == lm.shape[0] == cm.shape[0] and
            wm.shape[1] == lm.shape[1] == cm.shape[1]):
        raise ValueError("Window, local cost and cost matrices must have the same shape")

    cdef int nsteps = nstepsp[0]
    if nsteps < 1 or dir.shape[0] != 4 * nsteps:
        raise ValueError("Malformed step pattern description")
    pn = np.asarray(dir[:nsteps])
    if (np.any(pn != np.floor(pn)) or pn[0] < 1 or pn[-1] > nsteps or
            np.any(np.diff(pn) < 0)):
        raise ValueError("Step pattern numbers must be integers in ascending order, from 1")

    # Memory ordering is transposed (fortran-like in R).
    st = np.array([wm.shape[1],
                   wm.shape[0]], dtype=np.int32)
    cdef int [:] s = st

    sm = np.full_like(lm.base, -1, dtype=np.int32)

    with nogil:
        computeCM(&s[0],
                  &wm[0,0],
                  &lm[0,0],
                  &nstepsp[0],
                  &dir[0],
                  &cm[0,0],
                  &sm[0,0])

    return { 'costMatrix': cm.base,
             'directionMatrix': sm.base }



# Enumerate all the warping paths whose cumulative distance is within
# a threshold, following
#
#   Michael S. Waterman, Thomas H. Byers, A dynamic programming
#   algorithm to find all solutions in a neighborhood of the optimum,
#   Mathematical Biosciences, 77 (1985) 179-188.
#   doi:10.1016/0025-5564(85)90096-3
#
# Paths are grown backwards from the end cell(s) with a depth-first
# search. A step back from node N to the origin E of a pattern is
# taken only if
#
#     cost(N -> end) + cost(step) + costMatrix(E) <= threshold.
#
# Since costMatrix(E) is the cost of the best path reaching E, every
# partial path on the stack can be completed within the threshold: the
# search never enters a dead end, and its run time is proportional to
# the size of the output. Same algorithm as dtw_kbest.c in the R
# package.
#
# The step pattern comes as di, dj, sc (deltas and multipliers), with
# the rows of pattern k in first[k] .. first[k+1]-1, origin first.
# ends are the (0-based) columns where paths may end in the last row.
# Returns an unsorted list of (index1, index2, index1s, index2s,
# stepsTaken, distance) tuples.

def _nearOptimalPaths_search(const double [:,::1] lm not None,
                             const double [:,::1] cm not None,
                             const Py_ssize_t [::1] di not None,
                             const Py_ssize_t [::1] dj not None,
                             const double [::1] sc not None,
                             const Py_ssize_t [::1] first not None,
                             const Py_ssize_t [::1] ends not None,
                             double threshold,
                             Py_ssize_t max_paths):

    cdef Py_ssize_t n = cm.shape[0], m = cm.shape[1]
    if lm.shape[0] != n or lm.shape[1] != m:
        raise ValueError("Local cost and cost matrices must have the same shape")
    cdef Py_ssize_t npats = first.shape[0] - 1
    cdef Py_ssize_t nsteps = di.shape[0]
    if (npats < 1 or dj.shape[0] != nsteps or sc.shape[0] != nsteps or
            first[0] != 0 or first[npats] != nsteps):
        raise ValueError("Malformed step pattern description")

    # Every step decreases i+j, so a path has at most n+m-1 nodes,
    # and each one has at most npats pending siblings on the stack
    cdef Py_ssize_t maxlen = n + m
    cdef Py_ssize_t stacksize = ends.shape[0] + npats * maxlen
    cdef Py_ssize_t [::1] si = np.empty(stacksize, dtype=np.intp)
    cdef Py_ssize_t [::1] sj = np.empty(stacksize, dtype=np.intp)
    cdef Py_ssize_t [::1] sk = np.empty(stacksize, dtype=np.intp)
    cdef Py_ssize_t [::1] sdepth = np.empty(stacksize, dtype=np.intp)
    cdef double [::1] sdd = np.empty(stacksize, dtype=np.double)
    cdef Py_ssize_t top = 0

    # The path being formed, from the end backwards. bk[t] is the
    # pattern of the step from node t to node t-1.
    cdef Py_ssize_t [::1] bi = np.empty(maxlen, dtype=np.intp)
    cdef Py_ssize_t [::1] bj = np.empty(maxlen, dtype=np.intp)
    cdef Py_ssize_t [::1] bk = np.empty(maxlen, dtype=np.intp)

    cdef Py_ssize_t e, i, j, k, o, r, ei, ej, depth
    cdef double dd, test, c
    cdef unsigned long npops = 0
    out = []

    # Seed the stack with the end cells, last column at the bottom, so
    # that ties are found in the same order dtw() prefers
    for e in range(ends.shape[0] - 1, -1, -1):
        j = ends[e]
        if j < 0 or j >= m:
            raise ValueError("End column %d out of range" % j)
        c = cm[n - 1, j]
        if isfinite(c) and c <= threshold:
            si[top] = n - 1
            sj[top] = j
            sk[top] = -1
            sdepth[top] = 0
            sdd[top] = 0.0
            top += 1

    while top > 0:
        top -= 1
        i = si[top]
        j = sj[top]
        depth = sdepth[top]
        dd = sdd[top]

        npops += 1
        if npops % 65536 == 0:
            PyErr_CheckSignals()

        bi[depth] = i
        bj[depth] = j
        bk[depth] = sk[top]

        if i == 0 and j == 0:
            if len(out) >= max_paths:
                raise ValueError("More than %d paths are within the threshold. "
                                 "Decrease threshold or increase max_paths." % max_paths)
            out.append(_mkPath(lm, di, dj, sc, first, bi, bj, bk, depth))
            continue

        # Push in reverse, so that the first pattern is explored first
        for k in range(npats - 1, -1, -1):
            o = first[k]
            ei = i - di[o]
            ej = j - dj[o]
            if ei < 0 or ej < 0:
                continue
            # Cost of the step from the origin, excluding the origin.
            # Out-of-matrix cells are skipped, as in computeCM().
            test = dd
            for r in range(o + 1, first[k + 1]):
                if i - di[r] >= 0 and j - dj[r] >= 0:
                    test += sc[r] * lm[i - di[r], j - dj[r]]
            c = test + cm[ei, ej]
            if not (isfinite(c) and c <= threshold):
                continue
            if top >= stacksize:
                raise RuntimeError("Internal error: path stack overflow")
            si[top] = ei
            sj[top] = ej
            sk[top] = k
            sdepth[top] = depth + 1
            sdd[top] = test
            top += 1

    return out



# Build the output tuple for a complete path, whose nodes are bi[],
# bj[] from the end (0) to the start (d)
cdef _mkPath(const double [:,::1] lm,
             const Py_ssize_t [::1] di,
             const Py_ssize_t [::1] dj,
             const double [::1] sc,
             const Py_ssize_t [::1] first,
             const Py_ssize_t [::1] bi,
             const Py_ssize_t [::1] bj,
             const Py_ssize_t [::1] bk,
             Py_ssize_t d):

    cdef Py_ssize_t maxsteps = 0, k, r, t, ii, jj, ai, aj
    for k in range(first.shape[0] - 1):
        maxsteps = max(maxsteps, first[k + 1] - first[k])

    index1 = np.empty(d * maxsteps + 1, dtype=np.intp)
    index2 = np.empty(d * maxsteps + 1, dtype=np.intp)
    cdef Py_ssize_t [::1] fi = index1
    cdef Py_ssize_t [::1] fj = index2
    index1s = np.empty(d + 1, dtype=np.intp)
    index2s = np.empty(d + 1, dtype=np.intp)
    stepsTaken = np.empty(d, dtype=np.intp)
    cdef Py_ssize_t [::1] fis = index1s
    cdef Py_ssize_t [::1] fjs = index2s
    cdef Py_ssize_t [::1] fst = stepsTaken

    # Expand the steps into cells, and recompute the distance forward,
    # adding in the same order as computeCM() so that the best path
    # matches the dtw() distance exactly
    cdef Py_ssize_t ln = 0
    fi[ln] = 0
    fj[ln] = 0
    ln += 1
    cdef double cost = lm[0, 0]
    for t in range(d, 0, -1):
        k = bk[t]
        ai = bi[t - 1]
        aj = bj[t - 1]
        for r in range(first[k] + 1, first[k + 1]):
            ii = ai - di[r]
            jj = aj - dj[r]
            if ii < 0 or jj < 0:
                continue
            cost += sc[r] * lm[ii, jj]
            if di[r] != 0 or dj[r] != 0:
                fi[ln] = ii
                fj[ln] = jj
                ln += 1
        fi[ln] = ai
        fj[ln] = aj
        ln += 1

    for t in range(d + 1):
        fis[t] = bi[d - t]
        fjs[t] = bj[d - t]
    for t in range(d):
        fst[t] = bk[d - t] + 1      # 1-based, as in dtw()

    return (index1[:ln].copy(), index2[:ln].copy(),
            index1s, index2s, stepsTaken, cost)


    
  
def _test_computeCM(TS=5):

    DTYPE = np.int32
    
    twm = np.ones((TS, TS), dtype=DTYPE)

    tlm = np.zeros( (TS,TS), dtype=np.double)
    for i in range(TS):
        for j in range(TS):
            tlm[i,j]=(i+1)*(j+1)

    tnstepsp = np.array([6], dtype=DTYPE)

    tdir = np.array( (1, 1, 2, 2, 3, 3, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0,-1, 1,-1, 1,-1, 1),
                                     dtype=np.double)

    tcm = np.full_like(tlm, np.nan, dtype=np.double)
    tcm[0,0] = tlm[0,0]

    out = _computeCM_wrapper(twm,
                             tlm,
                             tnstepsp,
                             tdir,
                             tcm)
    return out
    
    
