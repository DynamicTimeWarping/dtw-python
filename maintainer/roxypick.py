#!/usr/bin/env python3

import glob
import sys
import re

rlist = glob.glob("../dtw/R/*.R")

roxy = []


def get_export(b):
    o = "UNKNOWN"
    for l in b:
        if l.startswith("@export"):
            try:
                o=l.split()[1]
            except:
                pass
    return o

def reformat(b):
    o = []
    p = []
    r = []
    for i,l in enumerate(b):
        if l.startswith("@note"):
            o.append("")
            o.append("Note")  
            o.append("----")
            l=l.replace("@note ","")
        if l.startswith("@param"):
            p.append({'name': l.split()[1],
                      'text': l.split()[2:] })
            l=""
        if l.startswith("@param"):

        o.append(l)
    return o
            


for rfile in rlist:
    with open(rfile) as rf:
        print(f"Parsing {rfile}...")
        inside = False
        current_block = []
        for line in rf:
            if line.startswith("#' "):
                inside = True
                line=line[3:]
                current_block.append(line.rstrip())
            else:
                if inside:
                    inside = False
                    export = get_export(current_block)
                    reformatted = reformat(current_block)
                    roxy.append({ 'file': rfile,
                                  'export': export,
                                  'text': reformatted })
                    current_block  = []

                
