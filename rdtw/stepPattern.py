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

class StepPattern:
    #IMPORT_RDOCSTRING stepPattern
    #ENDIMPORT

    def __init__(self, mx, hint="NA"):
        self.mx = numpy.array(mx, dtype=numpy.double)
        self.hint = hint

    def get_p(self):
        # Dimensions are reversed wrt R
        s = self.mx[:, [0, 2, 1, 3]]
        return s.T.reshape(-1)

    def get_n_rows(self):
        return self.mx.shape[0]

    def get_n_patterns(self):
        return int(numpy.max(self.mx[:,0]))

    def T(self):
        """ Transpose a step pattern. """
        tsp = self
        tsp.mx = tsp.mx[ : , [0,2,1,3] ]
        if tsp.hint == "N":
            tsp.hint = "M"
        elif tsp.hint == "M":
            tsp.hint = "N"
        return tsp

    def __repr__(self):
        np = self.get_n_patterns()
        head = " g[i,j] = min(\n"

        body = ""
        for p in range(1,np+1):
            steps = self._extractpattern(p)
            ns = steps.shape[0]
            steps = numpy.flip(steps,0)

            for s in range(ns):
                di, dj, cc = steps[s,:]
                dis = "" if di==0 else f"{-int(di)}"
                djs = "" if dj==0 else f"{-int(dj)}"
                dijs = f"i{dis:2},j{djs:2}"

                if cc==-1:
                    gs = f"    g[{dijs}]"
                    body = body + " " + gs
                else:
                    ccs = "    " if cc==1 else f"{cc:2.2g} *"
                    ds = f"+{ccs} d[{dijs}]"
                    body = body + " " + ds
            body = body + " ,\n"

        tail = " ) \n\n"
        ntxt = f"Normalization hint: {self.hint}\n"

        return "Step pattern recursion:\n"+head+body+tail+ntxt

    
    def plot(self):
        import matplotlib.pyplot as plt
        x = self.mx
        pats = 1+numpy.arange(self.get_n_patterns()+1)

        alpha = .5
        fudge = [0, 0]

        fig, ax = plt.subplots(figsize=(6, 6))
        for i in pats:
            ss = x[:,0] == i
            ax.plot(-x[ss,1],-x[ss,2], lw=2, color="tab:blue")
            ax.plot(-x[ss,1],-x[ss,2], 'o', color="black", marker="o", fillstyle="none" )

            if numpy.sum(ss)==1: continue

            xss = x[ss,:]
            xh = alpha * xss[:-1,1] + (1-alpha) * xss[1:,1]
            yh = alpha * xss[:-1,2] + (1-alpha) * xss[1:,2]

            for xx, yy, tt in zip(xh, yh, xss[1:,3]):
                ax.annotate( "{:.2g}".format(tt), (-xx-fudge[0],
                                                   -yy-fudge[1]))
            

        endpts = x[:,3] == -1
        ax.plot( -x[endpts,1], -x[endpts,2], 'o', color="black")
        
        ax.set_xlabel("Query index")
        ax.set_ylabel("Reference index")
        ax.set_xticks(numpy.unique(-x[:,1]))
        ax.set_yticks(numpy.unique(-x[:,2]))
        plt.show()
        return ax
    
        

    def _extractpattern(self, sn):
        sp = self.mx
        sbs = sp[:,0]==sn
        spl = sp[ sbs , 1:]
        return numpy.flip(spl,0)

    def _mkDirDeltas(self):
        out = numpy.array(self.mx, dtype=numpy.int32)
        out = out[ out[:,3] == -1, : ]
        out = out[:, [1,2]]
        return out
    
    

# Alternate constructor for ease of R import
def _c(*v):
    va = numpy.array([*v])
    if len(va) % 4 != 0:
        error("Internal error in _c constructor")
    va = va.reshape((-1,4))
    return(va)
    

##################################################
##################################################

# Reimplementation of the building process

class _P:
    def __init__(self, pid, subtype, smoothing):
        self.subtype = subtype
        self.smoothing = smoothing
        self.pid = pid
        self.i = [0]
        self.j = [0]

    def step(self, di, dj):  # equivalent to .Pstep
        self.i.append(di)
        self.j.append(dj)
        return self

    def get(self):             # eqv to .Pend
        ia = numpy.array(self.i, dtype=numpy.double)
        ja = numpy.array(self.j, dtype=numpy.double)
        si = numpy.cumsum(ia)
        sj = numpy.cumsum(ja)
        ni = numpy.max(si)-si # ?
        nj = numpy.max(sj)-sj
        if self.subtype == "a":
            w = numpy.minimum(ia, ja)
        elif self.subtype == "b":
            w = numpy.maximum(ia, ja)
        elif self.subtype == "c":
            w = ia
        elif self.subtype == "d":
            w = ia+ja
        else:
            error("Unsupported subtype")

        if self.smoothing:
            # if self.pid==3:                import ipdb; ipdb.set_trace()
            w[1:] = numpy.mean(w[1:])

        w[0] = -1.0

        nr = len(w)
        mx = numpy.zeros((nr,4))
        mx[:,0] = self.pid
        mx[:,1] = ni
        mx[:,2] = nj
        mx[:,3] = w
        return mx


def rabinerJuangStepPattern(ptype, slope_weighting="d", smoothed=False):
    #IMPORT_RDOCSTRING rabinerJuangStepPattern
    #ENDIMPORT

    f = {
        1: _RJtypeI,
        2: _RJtypeII,
        3: _RJtypeIII,
        4: _RJtypeIV,
        5: _RJtypeV,
        6: _RJtypeVI,
        7: _RJtypeVII
    }.get(ptype, lambda: error("Invalid type"))

    r = f(slope_weighting, smoothed)
    norm = "NA"
    if slope_weighting=="c":
        norm = "N"
    elif slope_weighting == "d":
        norm = "N+M"

    return StepPattern(r, norm)


def _RJtypeI(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,0).get(),
        _P(2, s, m).step(1,1).get(),
        _P(3, s, m).step(0,1).get() ] )

def _RJtypeII(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,1).step(1,0).get(),
        _P(2, s, m).step(1,1).get(),
        _P(3, s, m).step(1,1).step(0,1).get() ] )

def _RJtypeIII(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(2,1).get(),
        _P(2, s, m).step(1,1).get(),
        _P(3, s, m).step(1,2).get() ] )


def _RJtypeIV(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,1).step(1,0).get(),
        _P(2, s, m).step(1,2).step(1,0).get(),
        _P(3, s, m).step(1,1).get(),
        _P(4, s, m).step(1,2).get(),
    ] )

def _RJtypeV(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,1).step(1,0).step(1,0).get(),
        _P(2, s, m).step(1,1).step(1,0).get(),
        _P(3, s, m).step(1,1).get(),
        _P(4, s, m).step(1,1).step(0,1).get(),
        _P(5, s, m).step(1,1).step(0,1).step(0,1).get(),
    ] )


def _RJtypeVI(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,1).step(1,1).step(1,0).get(),
        _P(2, s, m).step(1,1).get(),
        _P(3, s, m).step(1,1).step(1,1).step(0,1).get()
    ] )

def _RJtypeVII(s,m):
    return numpy.vstack( [
        _P(1, s, m).step(1,1).step(1,0).step(1,0).get(),
        _P(2, s, m).step(1,2).step(1,0).step(1,0).get(),
        _P(3, s, m).step(1,3).step(1,0).step(1,0).get(),
        _P(4, s, m).step(1,1).step(1,0).get(),
        _P(5, s, m).step(1,2).step(1,0).get(),
        _P(6, s, m).step(1,3).step(1,0).get(),
        _P(7, s, m).step(1,1).get(),
        _P(8, s, m).step(1,2).get(),
        _P(9, s, m).step(1,3).get(),
    ] )



    
##########################################################################################
##########################################################################################

## Everything here is semi auto-generated from the R source. Don't
## edit!


##################################################
##################################################


##
## Various step patterns, defined as internal variables
##
## First column: enumerates step patterns.
## Second   	 step in query index
## Third	 step in reference index
## Fourth	 weight if positive, or -1 if starting point
##
## For \cite{} see dtw.bib in the package
##



## Widely-known variants

## White-Neely symmetric (default)
## aka Quasi-symmetric \cite{White1976}
## normalization: no (N+M?)
symmetric1 = StepPattern(_c(
                            1,1,1,-1,
                            1,0,0,1,
                            2,0,1,-1,
                            2,0,0,1,
                            3,1,0,-1,
                            3,0,0,1
                            ));


## Normal symmetric
## normalization: N+M
symmetric2 = StepPattern(_c(
                            1,1,1,-1,
                            1,0,0,2,
                            2,0,1,-1,
                            2,0,0,1,
                            3,1,0,-1,
                            3,0,0,1
                            ),"N+M");


## classic asymmetric pattern: max slope 2, min slope 0
## normalization: N
asymmetric =  StepPattern(_c(
                             1,1,0,-1,
                             1,0,0,1,
                             2,1,1,-1,
                             2,0,0,1,
                             3,1,2,-1,
                             3,0,0,1
                           ),"N");


# % \item{\code{symmetricVelichkoZagoruyko}}{symmetric, reproduced from %
# [Sakoe1978]. Use distance matrix \code{1-d}}
# 

## normalization: max[N,M]
## note: local distance matrix is 1-d
## \cite{Velichko}
_symmetricVelichkoZagoruyko = StepPattern(_c(
		1, 0, 1, -1,
		2, 1, 1, -1,
		2, 0, 0, -1.001,
		3, 1, 0, -1 ));


# % \item{\code{asymmetricItakura}}{asymmetric, slope contrained 0.5 -- 2
# from reference [Itakura1975]. This is the recursive definition % that
# generates the Itakura parallelogram; }
# 

## Itakura slope-limited asymmetric \cite{Itakura1975}
## Max slope: 2; min slope: 1/2
## normalization: N
_asymmetricItakura =  StepPattern(_c(
                        1, 1, 2, -1,
			1, 0, 0, 1,
			2, 1, 1, -1,
			2, 0, 0, 1,
			3, 2, 1, -1,
			3, 1, 0, 1,
			3, 0, 0, 1,
			4, 2, 2, -1,
			4, 1, 0, 1,
			4, 0, 0, 1
                       ));







#############################
## Slope-limited versions
##
## Taken from Table I, page 47 of "Dynamic programming algorithm
## optimization for spoken word recognition," Acoustics, Speech, and
## Signal Processing, vol.26, no.1, pp. 43-49, Feb 1978 URL:
## http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1163055
##
## Mostly unchecked



## Row P=0
symmetricP0 = symmetric2;

## normalization: N ?
asymmetricP0 = StepPattern(_c(
                                  1,0,1,-1,
                                  1,0,0,0,
                                  2,1,1,-1,
                                  2,0,0,1,
                                  3,1,0,-1,
                                  3,0,0,1
                                ),"N");


## alternative implementation
_asymmetricP0b = StepPattern(_c(
                                  1,0,1,-1,
                                  2,1,1,-1,
                                  2,0,0,1,
                                  3,1,0,-1,
                                  3,0,0,1
                                ),"N");



## Row P=1/2
symmetricP05 =  StepPattern(_c(
                        1  ,  1, 3 , -1,
                        1  ,  0, 2 ,  2,
                        1  ,  0, 1 ,  1,
                        1  ,  0, 0 ,  1,
                        2  ,  1, 2 , -1,
                        2  ,  0, 1 ,  2,
                        2  ,  0, 0 ,  1,
                        3  ,  1, 1 , -1,
                        3  ,  0, 0 ,  2,
                        4  ,  2, 1 , -1,
                        4  ,  1, 0 ,  2,
                        4  ,  0, 0 ,  1,
                        5  ,  3, 1 , -1,
                        5  ,  2, 0 ,  2,
                        5  ,  1, 0 ,  1,
                        5  ,  0, 0 ,  1
                               ),"N+M");

asymmetricP05 =  StepPattern(_c(
                        1  , 1 , 3 , -1,
                        1  , 0 , 2 ,1/3,
                        1  , 0 , 1 ,1/3,
                        1  , 0 , 0 ,1/3,
                        2  , 1 , 2 , -1,
                        2  , 0 , 1 , .5,
                        2  , 0 , 0 , .5,
                        3  , 1 , 1 , -1,
                        3  , 0 , 0 , 1 ,
                        4  , 2 , 1 , -1,
                        4  , 1 , 0 , 1 ,
                        4  , 0 , 0 , 1 ,
                        5  , 3 , 1 , -1,
                        5  , 2 , 0 , 1 ,
                        5  , 1 , 0 , 1 ,
                        5  , 0 , 0 , 1
                               ),"N");



## Row P=1
## Implementation of Sakoe's P=1, Symmetric algorithm

symmetricP1 = StepPattern(_c(
                              1,1,2,-1,	# First branch: g(i-1,j-2)+
                              1,0,1,2,	#            + 2d(i  ,j-1)
                              1,0,0,1,	#            +  d(i  ,j)
                              2,1,1,-1,	# Second branch: g(i-1,j-1)+
                              2,0,0,2,	#              +2d(i,  j)
                              3,2,1,-1,	# Third branch: g(i-2,j-1)+
                              3,1,0,2,	#            + 2d(i-1,j)
                              3,0,0,1	#            +  d(  i,j)
                        ),"N+M");

asymmetricP1 = StepPattern(_c(
                              1, 1 , 2 , -1 ,
                              1, 0 , 1 , .5 ,
                              1, 0 , 0 , .5 ,
                              2, 1 , 1 , -1 ,
                              2, 0 , 0 ,  1 ,
                              3, 2 , 1 , -1 ,
                              3, 1 , 0 ,  1 ,
                              3, 0 , 0 ,  1
                              ),"N");


## Row P=2
symmetricP2 = StepPattern(_c(
	1, 2, 3, -1,
	1, 1, 2, 2,
	1, 0, 1, 2,
	1, 0, 0, 1,
	2, 1, 1, -1,
	2, 0, 0, 2,
	3, 3, 2, -1,
	3, 2, 1, 2,
	3, 1, 0, 2,
	3, 0, 0, 1
),"N+M");

asymmetricP2 = StepPattern(_c(
	1, 2 , 3  , -1,
	1, 1 , 2  ,2/3,
	1, 0 , 1  ,2/3,
	1, 0 , 0  ,2/3,
	2, 1 , 1  ,-1 ,
	2, 0 , 0  ,1  ,
	3, 3 , 2  ,-1 ,
	3, 2 , 1  ,1  ,
	3, 1 , 0  ,1  ,
	3, 0 , 0  ,1
),"N");






################################
## Taken from Table III, page 49.
## Four varieties of DP-algorithm compared

## 1st row:  asymmetric

## 2nd row:  symmetricVelichkoZagoruyko

## 3rd row:  symmetric1

## 4th row:  asymmetricItakura




#############################
## Classified according to Rabiner
##
## Taken from chapter 2, Myers' thesis [4]. Letter is
## the weighting function:
##
##      rule       norm   unbiased
##   a  min step   ~N     NO
##   b  max step   ~N     NO
##   c  x step     N      YES
##   d  x+y step   N+M    YES
##
## Mostly unchecked

# R-Myers     R-Juang
# type I      type II   
# type II     type III
# type III    type IV
# type IV     type VII


typeIa =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  1,
                         1, 0, 0,  0,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1,  1,
                         3, 0, 0,  0
 ));

typeIb =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  1,
                         1, 0, 0,  1,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1,  1,
                         3, 0, 0,  1
 ));

typeIc =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  1,
                         1, 0, 0,  1,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1,  1,
                         3, 0, 0,  0
 ),"N");

typeId =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  2,
                         1, 0, 0,  1,
                         2, 1, 1, -1,
                         2, 0, 0,  2,
                         3, 1, 2, -1,
                         3, 0, 1,  2,
                         3, 0, 0,  1
 ),"N+M");

## ----------
## smoothed variants of above

typeIas =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0, .5,
                         1, 0, 0, .5,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1, .5,
                         3, 0, 0, .5
 ));


typeIbs =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  1,
                         1, 0, 0,  1,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1,  1,
                         3, 0, 0,  1
 ));


typeIcs =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0,  1,
                         1, 0, 0,  1,
                         2, 1, 1, -1,
                         2, 0, 0,  1,
                         3, 1, 2, -1,
                         3, 0, 1, .5,
                         3, 0, 0, .5
 ),"N");


typeIds =  StepPattern(_c(
                         1, 2, 1, -1,
                         1, 1, 0, 1.5,
                         1, 0, 0, 1.5,
                         2, 1, 1, -1,
                         2, 0, 0,  2,
                         3, 1, 2, -1,
                         3, 0, 1, 1.5,
                         3, 0, 0, 1.5
 ),"N+M");






## ----------

typeIIa = StepPattern(_c(
                        1,  1,  1, -1,
                        1,  0,  0, 1,
                        2,  1,  2, -1,
                        2,  0,  0, 1,
                        3,  2,  1, -1,
                        3,  0,  0, 1
                        ));

typeIIb = StepPattern(_c(
                        1,  1,  1, -1,
                        1,  0,  0, 1,
                        2,  1,  2, -1,
                        2,  0,  0, 2,
                        3,  2,  1, -1,
                        3,  0,  0, 2
                        ));

typeIIc = StepPattern(_c(
                        1,  1,  1, -1,
                        1,  0,  0, 1,
                        2,  1,  2, -1,
                        2,  0,  0, 1,
                        3,  2,  1, -1,
                        3,  0,  0, 2
                        ),"N");

typeIId = StepPattern(_c(
                        1,  1,  1, -1,
                        1,  0,  0, 2,
                        2,  1,  2, -1,
                        2,  0,  0, 3,
                        3,  2,  1, -1,
                        3,  0,  0, 3
                        ),"N+M");

## ----------

## Rabiner [3] discusses why this is not equivalent to Itakura's

typeIIIc =  StepPattern(_c(
                        1, 1, 2, -1,
			1, 0, 0, 1,
			2, 1, 1, -1,
			2, 0, 0, 1,
			3, 2, 1, -1,
			3, 1, 0, 1,
			3, 0, 0, 1,
			4, 2, 2, -1,
			4, 1, 0, 1,
			4, 0, 0, 1
                       ),"N");



## ----------

## numbers follow as production rules in fig 2.16

typeIVc =  StepPattern(_c(
                          1,  1,  1,  -1,
                          1,  0,  0,   1,
                          2,  1,  2,  -1,
                          2,  0,  0,   1,
                          3,  1,  3,  -1,
                          3,  0,  0,   1,
                          4,  2,  1,  -1,
                          4,  1,  0,   1,
                          4,  0,  0,   1,
                          5,  2,  2,  -1,
                          5,  1,  0,   1,
                          5,  0,  0,   1,
                          6,  2,  3,  -1,
                          6,  1,  0,   1,
                          6,  0,  0,   1,
                          7,  3,  1,  -1,
                          7,  2,  0,   1,
                          7,  1,  0,   1,
                          7,  0,  0,   1,
                          8,  3,  2,  -1,
                          8,  2,  0,   1,
                          8,  1,  0,   1,
                          8,  0,  0,   1,
                          9,  3,  3,  -1,
                          9,  2,  0,   1,
                          9,  1,  0,   1,
                          9,  0,  0,   1
 ),"N");






#############################
## 
## Mori's asymmetric step-constrained pattern. Normalized in the
## reference length.
##
## Mori, A.; Uchida, S.; Kurazume, R.; Taniguchi, R.; Hasegawa, T. &
## Sakoe, H. Early Recognition and Prediction of Gestures Proc. 18th
## International Conference on Pattern Recognition ICPR 2006, 2006, 3,
## 560-563
##

mori2006 =  StepPattern(_c(
                           1, 2, 1, -1,
                           1, 1, 0,  2,
                           1, 0, 0,  1,
                           2, 1, 1, -1,
                           2, 0, 0,  3,
                           3, 1, 2, -1,
                           3, 0, 1,  3,
                           3, 0, 0,  3
 ),"M");


## Completely unflexible: fixed slope 1. Only makes sense with
## open.begin and open.end
rigid = StepPattern(_c(1,1,1,-1,
                       1,0,0,1  ),"N")

