# -*- coding: utf-8 -*-

"""Console script for dtwr."""
import sys
import numpy
import dtwr
import argparse


def main2(query, reference, step_pattern):
    """Console script for dtwr."""

    out = "The Python and R interface provide the full functionality, including plots.\n"+\
          "See http://dtw.r-forge.r-project.org/\n\n"

    q = numpy.genfromtxt(query)
    r = numpy.genfromtxt(reference)
    al = dtwr.dtw(q, r, step_pattern=step_pattern)

    wp = numpy.vstack([al.index1, al.index2])

    try:
        out += f"Normalized distance: {al.normalizedDistance:.4g}\n\n"
    except:
        pass

    out += f"Distance: {al.distance:.4g}\n\n"
    out += f"Warping path: {wp}\n\n"

    return out

def main():
    parser = argparse.ArgumentParser(description='Command line DTW utility.')
    parser.add_argument("--query", default="query.csv", help="Query timeseries (tsv)")
    parser.add_argument("--reference", default="reference.csv", help="Reference timeseries (tsv)")
    parser.add_argument("--step_pattern", default="symmetric2", help="Step pattern, i.e. recursion rule")
    opts = parser.parse_args(sys.argv[1:])
    
    out=main2(opts.query, opts.reference, opts.step_pattern)
    print(out)
    

if __name__ == "__main__":
    main()

