#!/usr/bin/env python3



import rpy2
from rpy2.robjects.packages import importr

import glob
import sys
import re
import os
import pypandoc



# ==================================================
# Misc functions

def indent_as(l):
    """Return the indentation before hash"""
    c = l.find('#')
    return l[:c]

def dot_underscore(s):
    """R to Py"""
    rex = r"\b\.\b"
    s = re.sub(rex,"_",s)
    s = s.replace("TRUE","True")
    s = s.replace("FALSE","False")
    return s

def unarrow(s):
    s=s.replace("<-"," = ")
    return s


def getParameters(k):
    """Print out parameters list"""
    o=[]
    for i in range(1,len(k)+1):
        if k.rx(i).names[0] == "param":
            pn = dot_underscore(k.rx(i)[0][0][0])
            o.append(pn + " : ")
            o.append( "    " + k.rx(i)[0][1][0] )
    if len(o) > 0:
        out =  "Parameters\n"
        out += "----------\n"
        out += ("\n".join(o))
        return out
    else:
        return ""



def p(k,w,h=None):
    """Get section w of key k"""
    try:
        txt = k.rx2(w)[0]
        txt = dot_underscore(txt)
        txt_m = pypandoc.convert_text(txt,'rst',format="md")
        out = ""
        if h is not None:
            out = h + "\n"
            out += ("-" * len(h)) + "\n\n"
        out += txt_m + "\n\n"
        return out
    except:
        return ""


    
def getdoc(n):
    k=roxy[n]

    o=f"""\"\"\"{p(k,'title')}

{p(k,'description')}

**Details**

{p(k,'details')}

{getParameters(k)}

{p(k,'return','Returns')}

{p(k,'note','Notes')}

{p(k,'references','References')}

{getex(n)}
\"\"\"
"""
    o=sanitize_whitespace(o)
    return o

def sanitize_whitespace(o):
    """Remove duplicated empty lines"""
    return re.sub(r'\n\s*\n', '\n\n', o)


def convex(txt):
    o = []
    for l in txt.split("\n"):
        if l.startswith("##"):
            l = l.replace("#","")
            l = l.lstrip()
        elif re.match(r'^ *$',l):
            l = "\n"
        else:
            l = l.lstrip()
            l = dot_underscore(l)
            l = unarrow(l)
            l = ">>> "+l
        o.append(l)
    return "\n".join(o)


def getex(n):
    o=""
    try:
        with open(f"maintainer/examples/ex_{n}.py.txt") as f:
            o =  "Examples\n"
            o += "--------\n"
            o += f.read()
            o += "\n\n"
    except:
        print(f"No examples for {n}")
    return o



# ========================================
# ========================================






roxy = {}
pyex = {}

# ========================================
# Parse the roxygen headers

rlist = glob.glob("../dtw/R/*.R")

r2=importr("roxygen2")

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
# Write examples
for k in roxy:
    try:
        ex = roxy[k].rx2("examples")[0]
    except:
        continue
    with open(f"maintainer/examples/ex_{k}.R", "w") as f:
        print(f"Writing example: {k}")
        f.write(ex)
    with open(f"maintainer/examples/ex_{k}.py.draft", "w") as f:
        print(f"Writing draft: {k}")
        f.write(convex(ex))
    
    

print("\n\n")


# ==================================================
# Process all the python files

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
    
                    
