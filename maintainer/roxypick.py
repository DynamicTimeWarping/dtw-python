#!/usr/bin/env python3



import rpy2
from rpy2.robjects.packages import importr
r2=importr("roxygen2")

import glob
import sys
import re
import os
import pypandoc


rlist = glob.glob("../dtw/R/*.R")

roxy = {}


for rfile in rlist:
    print(f"Parsing {rfile}...")

    elts = r2.parse_file(rfile)

    for k in elts:
        try:
            # ex = k.rx2('export')[0]
            ex = k.slots['object'].rx2('alias')[0]
            print("found... "+ex)
        except:
            try:
                print("Using instead: "+k.rx2('name')[0])
                ex = k.rx2('name')[0]
            except:
                print("Real missing: "+rfile)
        roxy[ex] = k


print("\n\n")


# ==================================================

def indent_as(l):
    c = l.find('#')
    return l[:c]

def dot_underscore(s):
    rex = r"\b\.\b"
    return re.sub(rex,"_",s)


def getParameters(k):
    o=[]
    for i in range(1,len(k)+1):
        if k.rx(i).names[0] == "param":
            pn = dot_underscore(k.rx(i)[0][0][0])
            o.append(pn + " : ")
            o.append( "    " + k.rx(i)[0][1][0] )
    return "\n".join(o)



def p(k,w):
    try:
        txt = k.rx2(w)[0]
        txt = dot_underscore(txt)
        txt_m = pypandoc.convert_text(txt,'rst',format="md")
        return txt_m
    except:
        return "(None)"


    
def getdoc(n):
    k=roxy[n]

    o=f"""\"\"\"{p(k,'title')}

{p(k,'description')}

**Details**

{p(k,'details')}


Parameters
----------

{getParameters(k)}


Returns
-------

{p(k,'return')}


Notes
-----

{p(k,'note')}




\"\"\"
"""
    return o


# ==================================================






plist = glob.glob("dtwr/*.py")

for pfile in plist:
    print(f"Modifying {pfile}...")

    pfile_back = pfile+"~"
    os.rename(pfile, pfile_back )
    fin=open(pfile_back,"r")
    fout=open(pfile, "w")

    for l in fin:
        if "IMPORT_RDOCSTRING" in l:
            fout.write(l)       # Copy the tag

            fout.write(indent_as(l)) # Copy indentation

            n = l.split()[2]    # Extract name
            print(f" Inserting {n}")

            ds = getdoc(n)
            fout.write(ds)

            while True:         # Skip until the closing tag
                l = fin.readline()
                if "ENDIMPORT" in l:
                    fout.write(l)
                    break
        else:
            fout.write(l)

    fin.close()
    fout.close()
    
                    
