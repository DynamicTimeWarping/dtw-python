# -*- coding: utf-8 -*-

"""Console script for dtwr."""
import sys
import click
import numpy
import dtwr


@click.command()
@click.option("--query", default="query.csv", help="Query timeseries (tsv)")
@click.option("--reference", default="reference.csv", help="Reference timeseries (tsv)")
@click.option("--step_pattern", default="symmetric2", help="Step pattern, i.e. recursion rule")
def main(query, reference, step_pattern):
    """Console script for dtwr."""

    click.echo(
        "Command line DTW utility. The Python and R interface provide the full functionality, including plots.")
    click.echo("See http://dtw.r-forge.r-project.org/\n")
    q = numpy.genfromtxt(query)
    r = numpy.genfromtxt(reference)
    al = dtwr.dtw(q, r, step_pattern=step_pattern)

    wp = numpy.vstack([al.index1, al.index2])

    try:
        print(f"Normalized distance: {al.normalizedDistance:.4g}")
    except:
        pass

    print(f"Distance: {al.distance:.4g}")

    print(f"Warping path: {wp}")

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
