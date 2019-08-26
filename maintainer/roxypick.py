#!/usr/bin/env python3



import rpy2
from rpy2.robjects.packages import importr
r2=importr("roxygen2")

import glob
import sys
import re


rlist = glob.glob("../dtw/R/*.R")

roxy = {}


for rfile in rlist:
    print(f"Parsing {rfile}...")

    elts = r2.parse_file(rfile)

    for k in elts:
        try:
            ex = k.rx2('export')[0]
            print("found... "+ex)
        except:
            try:
                print("Not exported: "+k.rx2('name')[0])
            except:
                print("Real missing: "+rfile)
        roxy[ex] = k


    
