====================================================================
The Comprehensive Dynamic Time Warp package (Python bindings)
====================================================================


.. image:: https://img.shields.io/pypi/v/dtwr.svg
        :target: https://pypi.python.org/pypi/dtwr

.. image:: https://img.shields.io/travis/tonigi/dtwr.svg
        :target: https://travis-ci.org/tonigi/dtwr

.. image:: https://readthedocs.org/projects/dtwr/badge/?version=latest
        :target: https://dtwr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Comprehensive implementation of Dynamic Time Warping algorithms.
Supports arbitrary local (eg symmetric, asymmetric, slope-limited) and
global (windowing) constraints, fast native code, several plot styles,
and more.


Welcome
~~~~~~~

This package provides
the most complete, freely-available (GPL) implementation of Dynamic Time
Warping-type (DTW) algorithms up to date. It is a faithful Python equivalent
of `R's DTW package <http://dtw.r-forge.r-project.org/>`__.


The package is described in a `companion
paper <http://www.jstatsoft.org/v31/i07/>`__, including detailed
instructions and extensive background on things like multivariate
matching, open-end variants for real-time use, interplay between
recursion types and length normalization, history, etc.

Description
~~~~~~~~~~~

DTW is a family of algorithms which compute the local stretch or
compression to apply to the time axes of two timeseries in order to
optimally map one (query) onto the other (reference). DTW outputs the
remaining cumulative distance between the two and, if desired, the
mapping itself (warping function). DTW is widely used e.g. for
classification and clustering tasks in econometrics, chemometrics and
general timeseries mining.

The R implementation in `dtw <http://www.jstatsoft.org/v31/i07/>`__
provides:

-  arbitrary windowing functions (global constraints), eg. the
   `Sakoe-Chiba
   band <http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=01163055>`__
   and the `Itakura
   parallelogram <http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1162641>`__;
-  arbitrary transition types (also known as step patterns, slope
   constraints, local constraints, or DP-recursion rules). This includes
   dozens of well-known types:

   -  all step patterns classified by
      `Rabiner-Juang <http://www.worldcat.org/oclc/26674087>`__,
      `Sakoe-Chiba <http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=1163055>`__,
      and `Rabiner-Myers <http://hdl.handle.net/1721.1/27909>`__;
   -  symmetric and asymmetric;
   -  Rabiner's smoothed variants;
   -  arbitrary, user-defined slope constraints

-  partial matches: open-begin, open-end, substring matches
-  proper, pattern-dependent, normalization (exact average distance per
   step)
-  the Minimum Variance Matching (MVM) algorithm `(Latecki et
   al.) <http://dx.doi.org/10.1016/j.patcog.2007.03.004>`__

Multivariate timeseries can be aligned with arbitrary local distance
definitions, leveraging the *{proxy}dist* function. DTW itself becomes a
distance function with the *dist* semantics.

In addition to computing alignments, the package provides:

-  methods for plotting alignments and warping functions in several
   classic styles (see plot gallery);
-  graphical representation of step patterns;
-  functions for applying a warping function, either direct or inverse;
-  both fast native (C) and interpreted (R) cores.

Documentation
~~~~~~~~~~~~~

The best place to learn how to use the package (and a hopefully a decent
deal of background on DTW) is the companion paper `Computing and
Visualizing Dynamic Time Warping Alignments in R: The dtw
Package <http://www.jstatsoft.org/v31/i07/>`__, which the Journal of
Statistical Software makes available for free.

To have a look at how the *dtw* package is used in domains ranging from
bioinformatics to chemistry to data mining, have a look at the list of
`citing
papers <http://scholar.google.it/scholar?oi=bibs&hl=it&cites=5151555337428350289>`__.

A link to prebuilt documentation is
`here <http://www.rdocumentation.org/packages/dtw>`__.

Citation
~~~~~~~~

If you use *dtw*, do cite it in any publication reporting results
obtained with this software. Please follow the directions given in
``citation("dtw")``, i.e. cite:

   Toni Giorgino (2009). *Computing and Visualizing Dynamic Time Warping
   Alignments in R: The dtw Package.* Journal of Statistical Software,
   31(7), 1-24,
   `doi:10.18637/jss.v031.i07 <http://dx.doi.org/10.18637/jss.v031.i07>`__.

When using partial matching (unconstrained endpoints via the
``open.begin``/``open.end`` options) and/or normalization strategies,
please also cite:

   Paolo Tormene, Toni Giorgino, Silvana Quaglini, Mario Stefanelli
   (2008). Matching Incomplete Time Series with Dynamic Time Warping: An
   Algorithm and an Application to Post-Stroke Rehabilitation.
   Artificial Intelligence in Medicine, 45(1), 11-34.
   `doi:10.1016/j.artmed.2008.11.007 <http://dx.doi.org/10.1016/j.artmed.2008.11.007>`__


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
