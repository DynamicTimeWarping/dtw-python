
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

def plot(x, type, **kwargs):
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

    plot.show()
    return ax
    

def dtwPlotTwoWay(d, xts=None, yts=None,
                  offset=0,
                  ts.type="l",
                  match_indices=None,
                  match_col = "gray70",
                  xlab = "Index",
                  ylab = "Query value",
                  **kwargs):
    #IMPORT_RDOCSTRING dtwPlotTwoWay
    #ENDIMPORT

    import matplotlib.pyplot as plt

    if xts is None or yts is None:
        try:
            xts = d.query
            yts = d.reference
        except:
            error("Original timeseries are required")

    # ytso = yts + offset
    ytso = yts

    maxlen = max(len(xts),len(ytso))
    times = np.arange(maxlen)
    # xts = numpy.pad(xts,maxlen)
    # ytso = numpy.pad(ytso.maxlen)

    fig, ax = plt.subplots()
    if offset != 0:
        ax2 = ax.twinx()
    else:
        ax2 = ax

    ax.plot(times, xts, **kwargs)
    ax2.plot(times, yts, **kwargs)

    ql, qh = ax.get_ylim()
    rl, rh = ax2.get_ylim()
    
    if offset > 0:
        ax.set_ylim(ql-offset, qh)
        ax2.set_ylim(rl, rh+offset)
    elif offset < 0:
        ax.set_ylim(ql, qh+offset)
        ax2.set_ylim(rl-offset, rh)
        
    plt.show()
    return ax, ax2
    
        
