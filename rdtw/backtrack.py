# ----------------------------------------




import numpy 

# This is O(n). Let's not make it unreadable.
def _backtrack(gcm):
    n = gcm.N
    m = gcm.M
    i = n-1
    j = gcm.jmin

    iis=[i]; ii=[i];
    jjs=[j]; jj=[j];
    ss=[]

    # Drop null deltas
    dir = gcm.stepPattern.mx
    dir = dir[ numpy.bitwise_or( dir[:,1] != 0,
                              dir[:,2] != 0), : ]

    # Split by 1st column
    npat = gcm.stepPattern.get_n_patterns()
    stepsCache = dict()
    for q in range(1,npat+1):
        tmp = dir[ dir[:,0] == q, ]
        stepsCache[q] = numpy.array(tmp[:,[1,2]],
                                 dtype=numpy.int)
        

    while True:
        if i==0 and j==0: break

        # Direction taken, 1-based
        s = gcm.directionMatrix[i,j]

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


