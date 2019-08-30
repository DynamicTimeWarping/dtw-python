
import unittest

import numpy as np
from numpy import nan
from numpy.testing import (assert_approx_equal,
                           assert_array_equal, assert_raises)

from dtw import *


"""
# As in the JSS paper

ref <- window(aami3a, start = 0, end = 2)
test <- window(aami3a, start = 2.7, end = 5)
write.table(ref,"ref.dat",row.names=F,col.names=F)
write.table(test,"test.dat",row.names=F,col.names=F)
alignment <- dtw(test, ref, keep=T)
alignment$distance
"""

"""

warp> idx<-seq(0,6.28,len=100);

warp> query<-sin(idx)+runif(100)/10;

warp> reference<-cos(idx)

warp> alignment<-dtw(query,reference);

warp> wq<-warp(alignment,index.reference=FALSE);

warp> wt<-warp(alignment,index.reference=TRUE);

warp> old.par <- par(no.readonly = TRUE);

warp> par(mfrow=c(2,1));
"""



class TestDTW(unittest.TestCase):
    def test_sincos(self):
        idx = np.linspace(0,6.28,num=100)
        query = np.sin(idx) + np.random.uniform(size=100)/10.0
        reference = np.cos(idx)
        alignment = dtw(query,reference)
        
