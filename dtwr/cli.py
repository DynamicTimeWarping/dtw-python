# -*- coding: utf-8 -*-

"""Console script for dtwr."""
import sys
import click
import numpy
import dtwr


@click.command()
@click.option("--query",None,"Query timeseries (tsv)")
@click.option("--reference",None,"Reference timeseries (tsv)")
@click.option("--step_pattern","symmetric2","Step pattern, i.e. recursion rule")
def main(query, reference, step_pattern):
    """Console script for dtwr."""
    click.echo("Replace this message by putting your code into "
               "dtwr.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    q = numpy.genfromtxt(query)
    r = numpy.genfromtxt(reference)
    al = dtwr.dtw(q,r,step_pattern=step_pattern)

    wp = numpy.hstack([al.index1,al.index2])

    print(f"Distance: {al.distance}")
    try:
        print(f"Normalized distance: {al.normalizedDistance}")
    except:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
