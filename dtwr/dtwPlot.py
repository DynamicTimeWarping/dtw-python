
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
        
    lc = mc.LineCollection( col, linewidths=.5, colors=match_col )
    ax.add_collection(lc)
        
    plt.show()
    return ax, ax2
    
        
