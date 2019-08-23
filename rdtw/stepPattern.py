
import numpy

class StepPattern:
    def __init__(self, mx, hint):
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
        head = "g[i,j] = min(\n"

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
                    body = body + gs
                else:
                    ccs = "    " if cc==1 else f"{cc:2.2g}  *"
                    ds = f"+{ccs} d[{dijs}]"
                    body = body + ds
            body = body + ",\n"

        tail = ") \n\n"
        ntxt = f"Normalization hint: {self.hint}\n"

        return "Step pattern recursion:\n"+head+body+tail+ntxt
        

    def _extractpattern(self, sn):
        sp = self.mx
        sbs = sp[:,0]==sn
        spl = sp[ sbs , 1:]
        return numpy.flip(spl,0)

    

        

# TODO: all step patterns and generation functions
symmetric2 = StepPattern(numpy.array([[1, 1, 1, -1, ],
                                      [1, 0, 0, 2, ],
                                      [2, 0, 1, -1, ],
                                      [2, 0, 0, 1, ],
                                      [3, 1, 0, -1, ],
                                      [3, 0, 0, 1]]),
                         "N+M")

symmetric1 = StepPattern(numpy.array([[1, 1, 1, -1, ],
                                      [1, 0, 0, 1, ],
                                      [2, 0, 1, -1, ],
                                      [2, 0, 0, 1, ],
                                      [3, 1, 0, -1, ],
                                      [3, 0, 0, 1]]),
                         "NA")

asymmetric = StepPattern(numpy.array([[1, 1, 0, -1],
                                      [1, 0, 0, 1],
                                      [2, 1, 1, -1],
                                      [2, 0, 0, 1],
                                      [3, 1, 2, -1],
                                      [3, 0, 0, 1]]),
                         "N")

