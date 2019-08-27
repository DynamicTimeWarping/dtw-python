
##
## Copyright (c) 2006-2019 of Toni Giorgino
##
## This file is part of the DTW package.
##
## DTW is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## DTW is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.
##
## You should have received a copy of the GNU General Public License
## along with DTW.  If not, see <http://www.gnu.org/licenses/>.
##

import numpy

def dtwPlot(x, type, **kwargs):
    #IMPORT_RDOCSTRING plot.dtw
    """Plotting of dynamic time warp results


Methods for plotting dynamic time warp alignment objects returned by
[dtw()].


**Details**

``dtwPlot`` displays alignment contained in ``dtw`` objects.

Various plotting styles are available, passing strings to the ``type``
argument (may be abbreviated):

-  ``alignment`` plots the warping curve in ``d``;
-  ``twoway`` plots a point-by-point comparison, with matching lines;
   see [dtwPlotTwoWay()];
-  ``threeway`` vis-a-vis inspection of the timeseries and their warping
   curve; see [dtwPlotThreeWay()];
-  ``density`` displays the cumulative cost landscape with the warping
   path overimposed; see [dtwPlotDensity()]

If ``normalize`` is ``TRUE``, the *average* cost per step is plotted
instead of the cumulative one. Step averaging depends on the
[stepPattern()] used.

Additional parameters are carried on to the plotting functions: use with
care.



Parameters
----------

x,d : 
    `dtw` object, usually result of call to [dtw()]
xlab : 
    label for the query axis
ylab : 
    label for the reference axis
type : 
    general style for the alignment plot
plot_type : 
    type of line to be drawn, used as the `type` argument
in the underlying `plot` call
normalize : 
    show per-step average cost instead of cumulative cost
... : 
    additional arguments, passed to plotting functions


Returns
-------

(None)


Notes
-----

(None)




"""
    #ENDIMPORT

    if type == "alignment":
        dtwPlotAlignment(x,  **kwargs)
    elif type == "twoway":
        dtwPlotTwoWay(x,  **kwargs)
    elif type == "threeway":
        dtwPlotThreeWay(x,  **kwargs)
    elif type == "density":
        dtwPlotDensity(x,  **kwargs)



def dtwPlotAlignment(d, xlab="Query index", ylab="Reference index", **kwargs):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.plot( d.index1, d.index2, **kwargs)
    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    plt.show()
    return ax
    

def dtwPlotTwoWay(d, xts=None, yts=None,
                  offset=0,
                  ts_type="l",
                  match_indices=None,
                  match_col = "gray",
                  xlab = "Index",
                  ylab = "Query value",
                  **kwargs):
    #IMPORT_RDOCSTRING dtwPlotTwoWay
    """Plotting of dynamic time warp results: pointwise comparison


Display the query and reference time series and their alignment,
arranged for visual inspection.


**Details**

The two vectors are displayed via the [matplot()] functions; their
appearance can be customized via the ``type`` and ``pch`` arguments
(constants or vectors of two elements). If ``offset`` is set, the
reference is shifted vertically by the given amount; this will be
reflected by the *right-hand* axis.

Argument ``match_indices`` is used to draw a visual guide to matches; if
a vector is given, guides are drawn for the corresponding indices in the
warping curve (match lines). If integer, it is used as the number of
guides to be plotted. The corresponding style is customized via the
``match_col`` and ``match_lty`` arguments.

If ``xts`` and ``yts`` are not supplied, they will be recovered from
``d``, as long as it was created with the two-argument call of [dtw()]
with ``keep_internals=T``. Only single-variate time series can be
plotted this way.



Parameters
----------

d : 
    an alignment result, object of class `dtw`
xts : 
    query vector
yts : 
    reference vector
xlab,ylab : 
    axis labels
offset : 
    displacement between the timeseries, summed to reference
match_col,match_lty : 
    color and line type of the match guide lines
match_indices : 
    indices for which to draw a visual guide
ts_type,pch : 
    graphical parameters for timeseries plotting, passed to
`matplot`
... : 
    additional arguments, passed to `matplot`


Returns
-------

(None)


Notes
-----

When ``offset`` is set values on the left axis only apply to the query.





"""
    #ENDIMPORT

    import matplotlib.pyplot as plt
    from matplotlib import collections  as mc
    
    if xts is None or yts is None:
        try:
            xts = d.query
            yts = d.reference
        except:
            raise ValueError("Original timeseries are required")

    # ytso = yts + offset
    ytso = yts

    maxlen = max(len(xts),len(ytso))
    times = numpy.arange(maxlen)
    # xts = numpy.pad(xts,maxlen)
    # ytso = numpy.pad(ytso.maxlen)

    fig, ax = plt.subplots()
    if offset != 0:
        ax2 = ax.twinx()
        ax2.tick_params('y',colors='b')
    else:
        ax2 = ax

    ax.plot(times, xts, color='k', **kwargs)
    ax2.plot(times, yts, **kwargs)

    ql, qh = ax.get_ylim()
    rl, rh = ax2.get_ylim()
    
    if offset > 0:
        ax.set_ylim(ql-offset, qh)
        ax2.set_ylim(rl, rh+offset)
    elif offset < 0:
        ax.set_ylim(ql, qh-offset)
        ax2.set_ylim(rl+offset, rh)

    # https://stackoverflow.com/questions/21352580/matplotlib-plotting-numerous-disconnected-line-segments-with-different-colors
    if match_indices is None:
        idx = numpy.linspace(0, len(d.index1)-1)
    elif not hasattr(match_indices, "__len__"):
        idx = numpy.linspace(0, len(d.index1)-1, num=match_indices)
    else:
        idx = match_indices
    idx = numpy.array(idx).astype(int)

    col=[]
    for i in idx:
        col.append([ (d.index1[i], xts[d.index1[i]]),
                     (d.index2[i], -offset+yts[d.index2[i]]) ])
        
    lc = mc.LineCollection( col, linewidths=1, linestyles=":", colors=match_col )
    ax.add_collection(lc)
        
    plt.show()
    return ax, ax2
    
        

def dtwPlotThreeWay(d, xts=None, yts=None,
                    match_indices=None,
                    match_col = "gray",
                    xlab = "Query index",
                    ylab = "Reference index", **kwargs):
    #IMPORT_RDOCSTRING dtwPlotThreeWay
    """Plotting of dynamic time warp results: annotated warping function


Display the query and reference time series and their warping curve,
arranged for visual inspection.


**Details**

The query time series is plotted in the bottom panel, with indices
growing rightwards and values upwards. Reference is in the left panel,
indices growing upwards and values leftwards. The warping curve panel
matches indices, and therefore element (1,1) will be at the lower left,
(N,M) at the upper right.

Argument ``match_indices`` is used to draw a visual guide to matches; if
a vector is given, guides are drawn for the corresponding indices in the
warping curve (match lines). If integer, it is used as the number of
guides to be plotted. The corresponding style is customized via the
``match_col`` and ``match_lty`` arguments.

If ``xts`` and ``yts`` are not supplied, they will be recovered from
``d``, as long as it was created with the two-argument call of [dtw()]
with ``keep_internals=T``. Only single-variate time series can be
plotted.



Parameters
----------

d : 
    an alignment result, object of class `dtw`
xts : 
    query vector
yts : 
    reference vector
xlab : 
    label for the query axis
ylab : 
    label for the reference axis
main : 
    main title
type_align : 
    line style for warping curve plot
type_ts : 
    line style for timeseries plot
match_indices : 
    indices for which to draw a visual guide
margin : 
    outer figure margin
inner_margin : 
    inner figure margin
title_margin : 
    space on the top of figure
... : 
    additional arguments, used for the warping curve


Returns
-------

(None)


Notes
-----

(None)




"""
    #ENDIMPORT
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib import collections  as mc

    if xts is None or yts is None:
        try:
            xts = d.query
            yts = d.reference
        except:
            raise ValueError("Original timeseries are required")

    nn = len(xts)
    mm = len(yts)
    nn1 = numpy.arange(nn)
    mm1 = numpy.arange(mm)
        
    fig=plt.figure()
    gs=gridspec.GridSpec(2,2,
                         width_ratios=[1,3],
                         height_ratios=[3,1])
    axr=plt.subplot(gs[0])
    ax=plt.subplot(gs[1])
    axq=plt.subplot(gs[3])

    axq.plot(nn1, xts)          # query, horizontal, bottom
    axq.set_xlabel(xlab)
    
    axr.plot(yts, mm1)          # ref, vertical
    axr.invert_xaxis()
    axr.set_ylabel(ylab)

    ax.plot(d.index1, d.index2)

    if match_indices is None:
        idx = []
    elif not hasattr(match_indices, "__len__"):
        idx = numpy.linspace(0, len(d.index1)-1, num=match_indices)
    else:
        idx = match_indices
    idx = numpy.array(idx).astype(int)

    col=[]
    for i in idx:
        col.append([ (d.index1[i], 0),
                     (d.index1[i], d.index2[i]) ])
        col.append([ (0,d.index2[i]),
                     (d.index1[i], d.index2[i]) ])
        
    lc = mc.LineCollection( col, linewidths=1, linestyles=":", colors=match_col )
    ax.add_collection(lc)

    plt.show()
    return fig




def dtwPlotDensity(d, normalize=False,
                   xlab = "Query index",
                   ylab = "Reference index", **kwargs):
    #IMPORT_RDOCSTRING dtwPlotDensity
    """Display the cumulative cost landscape with the warping path overimposed


The plot is based on the cumulative cost matrix. It displays the optimal
alignment as a “ridge” in the global cost landscape.


**Details**

Normalization plots the average cost per step instead of the cumulative
cost. The alignment must have been constructed with the
``keep_internals=TRUE`` parameter set.



Parameters
----------

d : 
    an alignment result, object of class `dtw`
normalize : 
    whether to show the normalized cost
xlab : 
    label for the query axis
ylab : 
    label for the reference axis
... : 
    additional parameters forwarded to plotting functions


Returns
-------

(None)


Notes
-----

(None)




"""
    #ENDIMPORT
    import matplotlib.pyplot as plt

    try:
        cm = d.costMatrix
    except:
        raise ValueError("dtwPlotDensity requires dtw internals (set keep.internals=True on dtw() call)")

    if normalize:
        norm = d.stepPattern.hint
        row, col = numpy.indices( cm.shape )
        if norm == "NA":
            raise ValueError("Step pattern has no normalization")
        elif norm == "N":
            cm = cm / (row+1)
        elif norm == "N+M":
            cm = cm / (row+col+2)
        elif norm == "M":
            cm = cm / (col+1)

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.imshow(cm.T, origin="lower", cmap=plt.get_cmap("terrain"))
    co=ax.contour(cm.T, colors = "white")
    ax.clabel(co)

    ax.plot(d.index1, d.index2, color="blue", linewidth=2)

    ax.set_xlabel(xlab)
    ax.set_ylabel(ylab)

    plt.show()
    return ax

