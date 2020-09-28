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
    rex = r"([a-zA-Z])\.([a-zA-Z])"
    s = re.sub(rex,r"\1_\2",s)
    s = s.replace("TRUE","True")
    s = s.replace("FALSE","False")
    return s

def sanitize_rd_commands(s):
    """E.g. \doi"""
    import re
    s = re.sub('\\\\url{(.+?)}','<\\1>',s)
    s = re.sub('\\\\doi{(.+?)}','[doi:\\1](https://doi.org/\\1)',s)
    return s



def unarrow(s):
    s=s.replace("<-"," = ")
    return s


def getParameters(k):
    """Print out parameters list"""
    o=[]

    if "param" not in k:
        return ""
    
    for p in k['param']:
        pn = dot_underscore(p.rx2('name')[0])
        pd = dot_underscore(p.rx2('description')[0])
        pd = pd.replace("\n"," ")
        o.append(pn + " : ")
        o.append( "    " + pd )
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
        txt = "\n".join(k[w])
        txt = dot_underscore(txt)
        txt = sanitize_rd_commands(txt)
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

# For roxygen 7.1.1 this became elts[0].rx2("tags")[2].rx2("val")

rlist = glob.glob("../dtw/R/*.R")

r2=importr("roxygen2")

for rfile in rlist:
    print(f"Parsing {rfile}...")

    elts = r2.parse_file(rfile)
    for i,k in enumerate(elts):
        tagdict = {}
        for tag_r in k.rx2("tags"):
            tag = tag_r.rx2("tag")[0]
            val = tag_r.rx2("val")
            if tag not in tagdict:
                tagdict[tag] = []
            if tag == "param":
                tagdict[tag].append(val)
            else:
                tagdict[tag].append(val[0])
        try:
            ex = k.rx2('object').rx2('alias')[0]
            wh = "alias"
        except:
            try:
                ex = tagdict['name'][0]
                wh = "@name"
            except:
                print(f"  {i} NOT FOUND")
                continue
        
        print(f"  {i} found {wh}... "+ex)
        roxy[ex] = tagdict

print("\n\n")



# ==================================================
# Write examples
for k in roxy:
    try:
        ex = roxy[k]["examples"][0]
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

plist = glob.glob("dtw/*.py")

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
    
                    
