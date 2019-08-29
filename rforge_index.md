[![](images/thumbs/thumb_example12.png)](images/13.html)
[![](images/thumbs/thumb_example08.png)](images/9.html)
[![](images/thumbs/thumb_example18.png)](images/19.html)

# Welcome to Dynamic Time Warp project\!

Comprehensive implementation of Dynamic Time Warping algorithms in R.
Supports arbitrary local (eg symmetric, asymmetric, slope-limited) and
global (windowing) constraints, fast native code, several plot styles,
and more.

The R Package
[dtw](http://cran.r-project.org/web/packages/dtw/index.html) provides
the most complete, freely-available (GPL) implementation of Dynamic Time
Warping-type (DTW) algorithms up to date.

The package is described in a [companion
paper](http://www.jstatsoft.org/v31/i07/), including detailed
instructions and extensive background on things like multivariate
matching, open-end variants for real-time use, interplay between
recursion types and length normalization, history, etc.

### Description

DTW is a family of algorithms which compute the local stretch or
compression to apply to the time axes of two timeseries in order to
optimally map one (query) onto the other (reference). DTW outputs the
remaining cumulative distance between the two and, if desired, the
mapping itself (warping function). DTW is widely used e.g. for
classification and clustering tasks in econometrics, chemometrics and
general timeseries mining.

The R implementation in [dtw](http://www.jstatsoft.org/v31/i07/)
provides:

  - arbitrary windowing functions (global constraints), eg. the
    [Sakoe-Chiba
    band](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=01163055)
    and the [Itakura
    parallelogram](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1162641);
  - arbitrary transition types (also known as step patterns, slope
    constraints, local constraints, or DP-recursion rules). This
    includes dozens of well-known types:
      - all step patterns classified by
        [Rabiner-Juang](http://www.worldcat.org/oclc/26674087),
        [Sakoe-Chiba](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1163055),
        and [Rabiner-Myers](http://hdl.handle.net/1721.1/27909);
      - symmetric and asymmetric;
      - Rabiner's smoothed variants;
      - arbitrary, user-defined slope constraints
  - partial matches: open-begin, open-end, substring matches
  - proper, pattern-dependent, normalization (exact average distance per
    step)
  - the Minimum Variance Matching (MVM) algorithm [(Latecki et
    al.)](http://dx.doi.org/10.1016/j.patcog.2007.03.004)

Multivariate timeseries can be aligned with arbitrary local distance
definitions, leveraging the *{proxy}dist* function. DTW itself becomes a
distance function with the *dist* semantics.

In addition to computing alignments, the package provides:

  - methods for plotting alignments and warping functions in several
    classic styles (see plot gallery);
  - graphical representation of step patterns;
  - functions for applying a warping function, either direct or inverse;
  - both fast native (C) and interpreted (R) cores.

### Documentation

The best place to learn how to use the package (and a hopefully a decent
deal of background on DTW) is the companion paper [Computing and
Visualizing Dynamic Time Warping Alignments in R: The dtw
Package](http://www.jstatsoft.org/v31/i07/), which the Journal of
Statistical Software makes available for free.

To have a look at how the *dtw* package is used in domains ranging from
bioinformatics to chemistry to data mining, have a look at the list of
[citing
papers](http://scholar.google.it/scholar?oi=bibs&hl=it&cites=5151555337428350289).

A link to prebuilt documentation is
[here](http://www.rdocumentation.org/packages/dtw).

### Citation

If you use *dtw*, do cite it in any publication reporting results
obtained with this software. Please follow the directions given in
`citation("dtw")`, i.e. cite:

> Toni Giorgino (2009). *Computing and Visualizing Dynamic Time Warping
> Alignments in R: The dtw Package.* Journal of Statistical Software,
> 31(7), 1-24,
> [doi:10.18637/jss.v031.i07](http://dx.doi.org/10.18637/jss.v031.i07).

When using partial matching (unconstrained endpoints via the
`open.begin`/`open.end` options) and/or normalization strategies, please
also cite:

> Paolo Tormene, Toni Giorgino, Silvana Quaglini, Mario Stefanelli
> (2008). Matching Incomplete Time Series with Dynamic Time Warping: An
> Algorithm and an Application to Post-Stroke Rehabilitation. Artificial
> Intelligence in Medicine, 45(1), 11-34.
> [doi:10.1016/j.artmed.2008.11.007](http://dx.doi.org/10.1016/j.artmed.2008.11.007)

### Plot gallery

Go to a [gallery of sample plots](images/index.html) (straight out of
the examples in the documentation).

### Quickstart Example

[![](images/thumbs/thumb_example10.png)](images/11.html)

    ## A noisy sine wave as query
    idx<-seq(0,6.28,len=100);
    query<-sin(idx)+runif(100)/10;
    
    ## A cosine is for template; sin and cos are offset by 25 samples
    template<-cos(idx)
    
    ## Find the best match with the canonical recursion formula
    library(dtw);
    alignment<-dtw(query,template,keep=TRUE);
    
    ## Display the warping curve, i.e. the alignment curve
    plot(alignment,type="threeway")
    
    ## Align and plot with the Rabiner-Juang type VI-c unsmoothed recursion
    plot(
        dtw(query,template,keep=TRUE,
            step=rabinerJuangStepPattern(6,"c")),
        type="twoway",offset=-2);
    
    ## See the recursion relation, as formula and diagram
    rabinerJuangStepPattern(6,"c")
    plot(rabinerJuangStepPattern(6,"c"))
    
    ## And much more!  
    Try online

### Installation

To install the latest [stable
build](http://cran.r-project.org/web/packages/dtw/index.html) of the
package (hosted at CRAN), issue the following command in the R
console:  

    > install.packages("dtw")

  

To get started, begin from the installed documentation:  

    > library(dtw) 
    > demo(dtw)
    > ?dtw 
    > ?plot.dtw

  

### Frequently asked questions

*I've discovered a multidimensional/multivariate version of the DTW
algorithm\! Shall it be included in the package?*

> Alas, most likely you haven't. DTW had been "multidimensional" since
> its conception. Local distances are computed between *N*-dimensional
> vectors; feature vectors have been extensively used in speech
> recognition since the '70s (see e.g. things like MFCC, RASTA,
> cepstrum, etc). Don't worry: several other people have "rediscovered"
> multivariate DTW already. The *dtw* package supports the numerous
> types of multi-dimensional local distances that the
> [proxy](http://cran.r-project.org/web/packages/proxy/index.html)
> package does, as explained in section 3.6 of the [paper in
> JSS](http://www.jstatsoft.org/v31/i07/).

*I've discovered a realtime/early detection version of the DTW
algorithm\!*

> Alas, most likely you haven't. A natural solution for real-time
> recognition of timeseries is "unconstrained DTW", which relaxes one or
> both endpoint boundary conditions. To my knowledge, the algorithm was
> published as early as 1978 by [Rabiner, Rosenberg, and
> Levinson](http://dx.doi.org/10.1109/TASSP.1978.1163164) under the name
> UE2-1: see e.g. the mini-review in ([Tormene and Giorgino,
> 2008](http://dx.doi.org/10.1016/j.artmed.2008.11.007)). Feel also free
> to learn about the clever algorithms or expositions by [Sakurai et al.
> (2007)](http://dx.doi.org/10.1109/ICDE.2007.368963); [Latecki
> (2007)](http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=4470291);
> [Mori et al. (2006)](http://dx.doi.org/10.1109/ICPR.2006.467);
> [Smith-Waterman
> (1981)](http://dx.doi.org/10.1016%2F0022-2836%2881%2990087-5);
> [Rabiner and Schmidt
> (1980)](http://dx.doi.org/10.1109/TASSP.1980.1163422); etc. Open-ended
> alignments (at one or both ends) are available in the *dtw* package,
> as described in section 3.5 of the [JSS
> paper](http://www.jstatsoft.org/v31/i07/).

*I've discovered a bug in your backtrack algorithm\!*

> Alas, most likely you haven't. You may be doing backtracking via
> steepest descent. It's not the correct way to do it. Here's a
> counterexample:
> 
> ``` 
> > library(dtw) 
> > dm<-matrix(10,4,4)+diag(rep(1,4))
> > al<-dtw(dm,k=T,step=symmetric2)   
> > al$localCostMatrix
>       [,1] [,2] [,3] [,4]
> [1,]   11   10   10   10
> [2,]   10   11   10   10
> [3,]   10   10   11   10
> [4,]   10   10   10   11
> > al$costMatrix
>       [,1] [,2] [,3] [,4]
> [1,]   11   21   31   41
> [2,]   21   32   41   51
> [3,]   31   41   52   61
> [4,]   41   51   61   72
>       
> ```
> 
> The sum of costs along my warping path (blue) is (starting from
> \[1,1\]) 11+10+2\*10+2\*10+11 = 72 which is correct (=g\[4,4\]) . If
> you follow your backtracking "steepest descent" algorithm (red), you
> get the diagonal 11+2\*11+2\*11+2\*11=77 which is wrong.

*What's all the fuss about normalization? What's the problem with the
`symmetric1` recursion I found in Wikipedia/in another implementation?*

> An alignment computed with a non-normalizable step pattern has two
> serious drawbacks:
> 
> 1.  It cannot be meaningfully normalized by timeseries length. Hence,
>     longer timeseries have naturally higher distances, in turn making
>     comparisons impossible.
> 2.  It favors diagonal steps, therefore it is not robust: two paths
>     differing for a small local change (eg. horizontal+vertical step
>     rather than diagonal) have very different costs.
> 
> This is discussed in section 3.2 of the [JSS
> paper](http://www.jstatsoft.org/v31/i07/), section 4.2 of the [AIIM
> paper](http://dx.doi.org/10.1016/j.artmed.2008.11.007), section 4.7 of
> Rabiner and Juang's [Fundamentals of speech
> recognition](http://www.worldcat.org/oclc/26674087) book, and
> elsewhere. Make sure you familiarize yourself with those references.  
>   
> TLDR: just stick to the default `symmetric2` recursion and use the
> value of `normalizedDistance`.

*Can I use *dtw* in Python?*

> Yes. See Stefan Novak's [version of the quickstart
> example](http://stackoverflow.com/questions/5695388/dynamic-time-warping-in-python)
> on Stack Overflow. The mapping is performed through the Python package
> [rpy2](http://rpy2.bitbucket.org/), which makes the code natural and
> readable. It also reportedly plays well with *numpy*, *pandas* and
> *multiprocessing*. The following example has been updated for rpy2.
> 
>     import numpy as np
>     
>     import rpy2.robjects.numpy2ri
>     from rpy2.robjects.packages import importr
>     rpy2.robjects.numpy2ri.activate()
>         
>     # Set up our R namespaces
>     R = rpy2.robjects.r
>     DTW = importr('dtw')
>     
>     # Generate our data
>     idx = np.linspace(0, 2*np.pi, 100)
>     template = np.cos(idx)
>     query = np.sin(idx) + np.array(R.runif(100))/10
>     
>     # Calculate the alignment vector and corresponding distance
>     alignment = R.dtw(query, template, keep=True)
>     dist = alignment.rx('distance')[0][0]
>     
>     print(dist)

*What about *derivative* dynamic time warping?*

> See command
> [`diff`](http://stat.ethz.ch/R-manual/R-patched/library/base/html/diff.html).

*How do I choose a step pattern?*

> This question has been raised on Stack Overflow; see
> [here](http://stackoverflow.com/questions/30247132/r-dtw-package-cumulative-cost-matrix-decreases-at-some-points-along-the-path),
> [here](http://stats.stackexchange.com/questions/95920/searching-for-dynamic-time-warping-step-pattern)
> and
> [here](http://stackoverflow.com/questions/29399514/how-to-decide-which-steppattern-to-use-in-dtw-algorithm).
> A good first guess is `symmetric2` (the default), i.e.
> 
> ``` 
>          g[i,j] = min(
>              g[i-1,j-1] + 2 * d[i  ,j  ] ,
>              g[i  ,j-1] +     d[i  ,j  ] ,
>              g[i-1,j  ] +     d[i  ,j  ] ,
>          )
>      
> ```

*What is the relation between `dist` and `dtw`?*

> There are two *very different*, *totally unrelated* uses for `dist`.
> This is explained at length in the paper, but let's summarize.
> 
> 1.  If you have **two multivariate** timeseries, you can feed them to
>     `dist` to obtain a *local distance matrix*. You then pass this
>     matrix to dtw(). This is equivalent to passing the two matrices to
>     the dtw() function and specifying a `dist.method` (see also the
>     next question).
> 2.  If you have **many univariate** timeseries, instead of iterating
>     over all pairs and applying dtw() to each, you may feed the lot
>     (arranged as a matrix) to `dist` with `method="DTW"`. In this case
>     your code does NOT explicitly call dtw(). This is equivalent to
>     iterating over all pairs; it is also equivalent to using the
>     `dtwDist` convenience function.

*Why do changes in `dist.method` appear to have no effect?*

> Because it only makes a difference when aligning *multivariate*
> timeseries. It specifies the "pointwise" or local distance used
> (before the alignment) between the query feature *vector* at time *i*,
> `query[i,]` and the reference feature *vector* at time *j*, `ref[j,]`
> . Most distance functions coincide with the Euclidean distance in the
> one-dimensional case. Note the following:
> 
> ``` 
> r<-matrix(runif(10),5)  # A 2-D timeseries of length 5
> s<-matrix(runif(10),5)  # Ditto
> 
> myMethod<-"Manhattan" # Or anything else
> al1<-dtw(r,s,dist.method=myMethod)              # Passing the two inputs
> al2<-dtw(proxy::dist(r,s,method=myMethod))      # Equivalent, passing the distance matrix
> 
> all.equal(al1,al2) 
>      
> ```

*Can the time/memory requirements be relaxed?*

> The first thing you should try is to set the `distance.only=TRUE`
> parameter, which skips backtracing and some object copies. Second,
> consider downsampling the input timeseries.

### Clustering FAQ

*Can I use the DTW distance to cluster timeseries?*

> Of course. You need to start with a dissimilarity matrix, i.e. a
> matrix holding in *i,j* the DTW distance between timeseries *i* and
> *j*. This matrix is fed to the clustering functions. Obtaining the
> dissimilarity matrix is done differently depending on whether your
> timeseries are univariate or or multivariate: see the next questions.

*How do I cluster univariate timeseries of homogeneous length?*

> Arrange the timeseries (single-variate) in a matrix *as rows*. Make
> sure you use a symmetric pattern. See
> [dtwDist](http://www.rdocumentation.org/packages/dtw/functions/dtwDist).

*How do I cluster *multiple* *multivariate* timeseries?*

> You have to handle the loop yourself. Assuming you have data arranged
> as `x[time,component,series]`, pseudocode would be:
> 
> ``` 
>  for (i in 1:N) { 
>     for (j in 1:N) { 
>         result[i,j] <- dtw( dist(x[,,i],x[,,j]), distance.only=T )$normalizedDistance 
> ```

*Can I compute a DTW-based dissimilarity matrix out of timeseries of
different lengths?*

> Either loop over the inputs yourself, or pad with NAs and use the
> following code:
> 
>     dtwOmitNA <-function (x,y)
>     {
>         a<-na.omit(x)
>         b<-na.omit(y)
>         return(dtw(a,b,distance.only=TRUE)$normalizedDistance)
>     }
>     
>     ## create a new entry in the registry with two aliases
>     pr_DB$set_entry(FUN = dtwOmitNA, names = c("dtwOmitNA"))
>     
>     d<-dist(dataset, method = "dtwOmitNA") 

### License

This software is distributed under the terms of the GNU General Public
License Version 2, June 1991. The terms of this license are in a file
called COPYING which you should have received with this software and
which can be displayed by ` RShowDoc("COPYING")`.

### Contact

[Toni dot Giorgino](https://sites.google.com/site/tonigiorgino/) at
gmail.com  
  
Istituto di Neuroscienze (ISIB-IN-CNR)  
Consiglio Nazionale delle Ricerche  
Padova, Italy  
  
Academic and public research institutions are welcome to invite me for
discussions or seminars. Please indicate dates, preferred format, and
audience type.

### Commercial support

I am also interested in hearing from companies seeking to use DTW in a
commercial setting. I may provide on-site and/or remote consultancy
through the [Istituto di Biofisica](http://www.ibf.cnr.it/).

  
  
  
  
  
$Id: index.php 441 2019-07-31 06:53:16Z tonig $
