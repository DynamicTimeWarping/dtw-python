
import numpy

class StepPattern:
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
                    gs = f"  g[{dijs}]"
                    body = body + " " + gs
                else:
                    ccs = "    " if cc==1 else f"{cc:2.2g} *"
                    ds = f"+{ccs} d[{dijs}]"
                    body = body + " " + ds
            body = body + " ,\n"

        tail = " ) \n\n"
        ntxt = f"Normalization hint: {self.hint}\n"

        return "Step pattern recursion:\n"+head+body+tail+ntxt
        

    def _extractpattern(self, sn):
        sp = self.mx
        sbs = sp[:,0]==sn
        spl = sp[ sbs , 1:]
        return numpy.flip(spl,0)

    

# Alternate constructor for ease of R import
def _c(*v):
    va = numpy.array([*v])
    if len(va) % 4 != 0:
        error("Internal error in _c constructor")
    va = va.reshape((-1,4))
    return(va)
    


    
##################################################
##################################################

## Everything here is auto-generated from the R source



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

