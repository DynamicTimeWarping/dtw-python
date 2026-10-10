##
## Copyright (c) 2006-2026 of Toni Giorgino
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

"""DTW permutation test"""

import numbers
import warnings

import numpy
import scipy.spatial.distance
import scipy.stats

from dtw.dtw import DTW, dtw
from dtw.window import noWindow

__all__ = ["PermutationTestResult", "permutationTest"]


_CORRELATIONS = ("pearson", "spearman", "kendall")
_STATISTICS = ("distance", "normalizedDistance") + _CORRELATIONS


class PermutationTestResult:
    """The result of a DTW permutation test, returned by [permutationTest()].

**Attributes:**

- ``statistic`` the name of the statistic
- ``estimate`` the observed value of the statistic
- ``p_value`` the permutation p-value
- ``replicates`` the number of permutation replicates
- ``alternative`` the alternative hypothesis
- ``method`` a description of the test
- ``null_distribution`` the simulated statistics, if requested with
  ``return_distribution=True``; ``None`` otherwise

"""

    def __init__(self, obj):
        self.__dict__.update(obj)

    def __repr__(self):
        return ("{}\n"
                "{} = {:.7g}, p-value = {:.4g}\n"
                "alternative hypothesis: {}").format(self.method,
                                                     self.statistic, self.estimate,
                                                     self.p_value, self.alternative)


# Shuffle increment rows, retaining matrix dimensions even for singleton input.
def _permute_derivative(x, rng):
    if x.shape[0] <= 1:
        return x
    dx = numpy.diff(x, axis=0)
    ridx = rng.permutation(dx.shape[0])
    return numpy.cumsum(numpy.vstack([x[:1, :], dx[ridx, :]]), axis=0)


def _compute_statistic(al, statistic, query, reference):
    if statistic == "distance":
        return al.distance
    elif statistic == "normalizedDistance":
        return al.normalizedDistance
    elif statistic in _CORRELATIONS:
        wq = query[al.index1, 0]
        wr = reference[al.index2, 0]
        # Only the coefficient is needed; the analytical p-value does not
        # account for the alignment or repeated observations along a path.
        with warnings.catch_warnings(), numpy.errstate(all="ignore"):
            warnings.simplefilter("ignore")
            if len(wq) < 2:
                return numpy.nan
            if statistic == "pearson":
                return numpy.corrcoef(wq, wr)[0, 1]
            elif statistic == "spearman":
                return scipy.stats.spearmanr(wq, wr)[0]
            else:
                return scipy.stats.kendalltau(wq, wr)[0]
    else:
        raise ValueError("Internal error: unexpected statistic argument")


def permutationTest(alignment,
                    R=1000,
                    alternative=None,
                    permute_side="query",
                    permute_what="values",
                    statistic="distance",
                    return_distribution=False,
                    rng=None):
    """DTW permutation test

Compare an observed DTW statistic with statistics obtained by permuting
values or increments of the query, reference, or both, and recomputing
the alignment for every replicate. The choice of permutation defines the
null hypothesis and determines the interpretation of the returned
p-value.

**Details**

The comparison asks: how unusually small is the observed DTW distance
relative to distances obtained after randomly reordering the query,
reference, or both? Correlation statistics instead assess how unusually
large the correlation between the aligned series is.

Each replicate permutes either the observations
(``permute_what="values"``) or their consecutive increments
(``permute_what="increments"``), then computes a new optimal alignment.
The resulting statistics form a simulated distribution under the
selected null hypothesis. The observed statistic is compared with this
distribution, rather than with distances along the original, fixed
warping path.

The ``statistic`` argument selects the ordinary DTW distance, its
normalized counterpart, or a correlation coefficient between the aligned
univariate series. Setting ``return_distribution=True`` includes the
simulated statistics in the result's ``null_distribution`` attribute,
allowing them to be plotted alongside the observed statistic.

The scientific interpretation depends on which reorderings are assumed
possible under the null. See **Null hypotheses** and **Interpretation**,
and consult **Requirements** before using the reported p-value.

**Null hypotheses**

Both methods permute without replacement within each replicate.
Permutations are sampled independently across replicates, so the same
permutation can occur more than once, including the original ordering.

With ``permute_what="values"``, the null assumes that, conditional on
the observed values, all temporal orderings of the shuffled series are
equally likely. This exchangeability must also hold conditional on the
unshuffled series when one side is held fixed. Independent, identically
distributed observations independent of the other series satisfy this
assumption. The permutation preserves the observed value distribution
but destroys temporal structure such as autocorrelation, trends, and
cycles. For multivariate series, entire observation rows are permuted
together, preserving the relationships between components within each
row.

With ``permute_what="increments"``, the null assumes that, conditional
on the starting value and observed increments, all orderings of those
increments are equally likely, also conditional on any fixed opposite
series. The increments are consecutive differences,
``numpy.diff(x, axis=0)``, without division by time intervals. They are
permuted and cumulatively summed from the original starting value. This
preserves the increment distribution and both endpoints (up to numerical
precision), but generally changes the distribution of the series'
values. Multivariate increment rows are permuted together. A random walk
with independent, identically distributed increments, independent of
the other series, is one setting where this assumption is appropriate.
Correlated increments, mean reversion, oscillations, or changing
increment distributions can violate it. Preserving endpoints does not
make this method generally more conservative than value permutation.

``permute_side="query"`` holds the reference fixed; ``"reference"``
holds the query fixed. With ``"both"``, the two series are permuted
independently, and the null requires invariance under these independent
reorderings. Choosing a different side can change the null distribution
and the assumptions needed.

**Interpretation**

For a distance statistic, the usual alternative is ``"less"``: the
observed distance is unusually small relative to the chosen permutation
distribution. ``"greater"`` asks whether it is unusually large, and
``"two-sided"`` considers both tails. For correlation statistics, the
usual alternative is ``"greater"``. Each replicate is realigned before
computing its correlation; the null correlation distribution need not be
centered at zero.

Neither permutation scheme provides a general test of independence
between arbitrary time series. Independent smooth series can align
better than shuffled series because of their temporal structure. With a
correctly calibrated test, a small p-value is evidence against the
specified permutation null; it does not by itself establish dependence
or a scientifically meaningful correspondence. A large p-value indicates
insufficient evidence against that null, rather than evidence that the
series have no temporal ordering.

Choose the null from the scientific question and sampling process before
examining results. Neither the default ``"values"`` nor ``"increments"``
is appropriate for every time series. In particular, increment
permutation of independent, identically distributed observations is
invalid: their increments are negatively autocorrelated, and reordering
them produces random walks that wander far from the original values.
Other designs may call for permutation of whole-series pairings across
exchangeable trials, calibrated time-shift tests, block permutations, or
Fourier surrogates that preserve spectral structure. These methods have
their own assumptions and are not implemented here. See Schreiber and
Schmitz (2000) for a discussion of surrogate methods and their
interpretation.

**P-value calculation**

For ``alternative="less"``, let ``b`` count simulated statistics less
than or equal to the observed statistic. For ``"greater"``, count those
greater than or equal to it. The respective one-sided p-value is
``(b + 1) / (R + 1)``. This includes the observed ordering and prevents
zero p-values from a finite simulation; see Phipson and Smyth (2010). To
accommodate numerical roundoff, statistics within
``100 * eps * max(1, abs(observed))`` of the observed statistic, where
``eps`` is the machine epsilon, are counted as ties in both tails.

The two-sided p-value is twice the smaller of these one-sided p-values,
capped at one. This convention does not assume a symmetric null
distribution. Tied distributions give a p-value of one when all
replicates match the observed statistic. The correction does not
compensate for an inappropriate null model; the exchangeability
assumptions still apply.

**Requirements**

Step patterns, open-begin/open-end settings, the window function and its
``window_args`` are reused for every alignment. Increment permutation
also requires the stored distance method. Custom window functions must
reproduce the original window; avoid functions whose behavior depends on
mutable external state. Choose alignment settings before inspecting test
results.

Correlation statistics require the original univariate series. If the
input was constructed with ``distance_only=True``, its path is
recomputed. Both the observed statistic and every simulated statistic
must be finite. Undefined correlations, for example from constant
aligned series or fewer than two aligned observations, cause an error.
Failed replicates are not discarded or resampled. A series of length one
can be used for distance statistics; permuting its increments leaves it
unchanged.

Results are reproducible by passing a seed or a
``numpy.random.Generator`` as ``rng``. The random streams differ from
R's, so the R and Python packages give different (but equally valid)
null distributions for the same seed.

Parameters
----------
alignment :
    An object of class `DTW`, constructed with ``keep_internals=True``. Increment permutation and correlation statistics additionally require the original query and reference; an alignment computed from a precomputed local cost matrix is insufficient.
R :
    Number of permutation replicates, a positive integer.
alternative :
    ``None`` (the default) selects ``"less"`` for distance statistics and ``"greater"`` for correlations. Alternatively, a string: ``"less"`` for unusually small distances, ``"greater"`` for unusually large distances, or ``"two-sided"`` for either tail. For correlations these directions refer to the correlation coefficient, rather than the distance.
permute_side :
    Which series to permute: ``"query"``, ``"reference"``, or independently ``"both"``. See **Null hypotheses**.
permute_what :
    What to permute: observation values (``"values"``, the default) or consecutive increments (``"increments"``). Neither choice is a general null model for unrelated time series.
statistic :
    ``"distance"`` for the DTW distance or ``"normalizedDistance"`` for its normalized counterpart. The latter requires a normalizable step pattern. ``"pearson"``, ``"spearman"``, and ``"kendall"`` select the corresponding correlation coefficient between the aligned univariate series.
return_distribution :
    If ``True``, include the simulated statistics as the ``null_distribution`` attribute of the result. This does not validate the chosen null model.
rng :
    Seed or ``numpy.random.Generator`` used for the permutations, passed to ``numpy.random.default_rng``.

Returns
-------

A [PermutationTestResult] object, with the observed statistic in
``estimate``, the permutation p-value in ``p_value`` and the number of
replicates in ``replicates``. If ``return_distribution=True``, its
``null_distribution`` attribute is a numeric array of length ``R``
containing the simulated statistics; otherwise it is ``None``.

References
----------

1. Schreiber, T. and Schmitz, A. (2000). Surrogate time series. *Physica
   D*, 142, 346–382.
   `doi:10.1016/S0167-2789(00)00043-9 <https://doi.org/10.1016/S0167-2789(00)00043-9>`__
2. Phipson, B. and Smyth, G. K. (2010). Permutation P-values should never
   be zero: calculating exact P-values when permutations are randomly
   drawn. *Statistical Applications in Genetics and Molecular Biology*,
   9, Article 39.
   `doi:10.2202/1544-6115.1585 <https://doi.org/10.2202/1544-6115.1585>`__

Examples
--------
>>> from dtw import *
>>> import numpy as np
>>> rng = np.random.default_rng(123)

Value permutation: independent observations with exchangeable ordering.

>>> al_values = dtw(rng.normal(size=40), rng.normal(size=40),
...                 keep_internals=True)
>>> res = permutationTest(al_values, R=199, permute_what="values", rng=rng)
>>> 0 < res.p_value <= 1
True
>>> d_values = permutationTest(
...     al_values, R=199, alternative="less", permute_side="query",
...     permute_what="values", statistic="normalizedDistance",
...     return_distribution=True, rng=rng).null_distribution

Increment permutation: independent walks with exchangeable increments.

>>> query = np.concatenate([[0], np.cumsum(rng.normal(size=39))])
>>> reference = np.concatenate([[0], np.cumsum(rng.normal(size=39))])
>>> al_walk = dtw(query, reference, keep_internals=True)
>>> d_walk = permutationTest(
...     al_walk, R=199, alternative="less", permute_side="query",
...     permute_what="increments", statistic="normalizedDistance",
...     return_distribution=True, rng=rng).null_distribution

Each observed distance is compared with its own permutation distribution.

>>> import matplotlib.pyplot as plt                       # doctest: +SKIP
>>> fig, (ax1, ax2) = plt.subplots(1, 2)                  # doctest: +SKIP
>>> ax1.hist(d_values, bins=20)                           # doctest: +SKIP
>>> ax1.axvline(al_values.normalizedDistance, ls="--")    # doctest: +SKIP
>>> ax1.set_title("Value permutation")                    # doctest: +SKIP
>>> ax2.hist(d_walk, bins=20)                             # doctest: +SKIP
>>> ax2.axvline(al_walk.normalizedDistance, ls="--")      # doctest: +SKIP
>>> ax2.set_title("Increment permutation")                # doctest: +SKIP

"""

    if permute_side not in ("query", "reference", "both"):
        raise ValueError("permute_side must be one of 'query', 'reference', 'both'")
    if permute_what not in ("values", "increments"):
        raise ValueError("permute_what must be one of 'values', 'increments'")
    if statistic not in _STATISTICS:
        raise ValueError("statistic must be one of " + ", ".join(repr(s) for s in _STATISTICS))
    correlation = statistic in _CORRELATIONS
    if alternative is None:
        alternative = "greater" if correlation else "less"
    if alternative not in ("less", "greater", "two-sided"):
        raise ValueError("alternative must be one of 'less', 'greater', 'two-sided'")

    if not isinstance(alignment, DTW):
        raise TypeError("alignment must be an object of class DTW")
    if (not isinstance(R, numbers.Real) or isinstance(R, bool) or
            not numpy.isfinite(R) or R < 1 or R != numpy.floor(R)):
        raise ValueError("R must be a positive integer")
    R = int(R)
    if not isinstance(return_distribution, (bool, numpy.bool_)):
        raise ValueError("return_distribution must be True or False")
    if not hasattr(alignment, "localCostMatrix"):
        raise ValueError("The alignment must be constructed with keep_internals=True")

    lcm = numpy.asarray(alignment.localCostMatrix)
    if lcm.ndim != 2 or not numpy.issubdtype(lcm.dtype, numpy.number) or 0 in lcm.shape:
        raise ValueError("alignment must contain a nonempty numeric local cost matrix")
    if statistic == "normalizedDistance" and alignment.stepPattern.hint == "NA":
        raise ValueError("normalizedDistance requires a normalizable step pattern")

    query = getattr(alignment, "query", None)
    reference = getattr(alignment, "reference", None)
    if permute_what == "increments" or correlation:
        if query is None or reference is None:
            raise ValueError("Increment permutation and correlation statistics require original "
                             "query and reference series; rebuild the alignment from the series "
                             "with keep_internals=True")
        query = numpy.asarray(query)
        reference = numpy.asarray(reference)
        if (query.ndim != 2 or reference.ndim != 2 or
                not numpy.issubdtype(query.dtype, numpy.number) or
                not numpy.issubdtype(reference.dtype, numpy.number) or
                query.shape[0] != lcm.shape[0] or reference.shape[0] != lcm.shape[1] or
                query.shape[1] == 0 or reference.shape[1] == 0 or
                not numpy.all(numpy.isfinite(query)) or
                not numpy.all(numpy.isfinite(reference))):
            raise ValueError("The retained series must be finite numeric matrices "
                             "matching the local cost matrix")
    if correlation and (query.shape[1] != 1 or reference.shape[1] != 1):
        raise ValueError("Correlation statistics require univariate query and reference series")
    if permute_what == "increments" and getattr(alignment, "distanceMethod", None) is None:
        raise ValueError("The alignment has no stored distance method; "
                         "rebuild it with the current dtw version")

    window_args = getattr(alignment, "windowArgs", None)
    if window_args is None:
        if alignment.windowFunction != noWindow:
            raise ValueError("The alignment has no stored window arguments; "
                             "rebuild it with the current dtw version")
        window_args = {}

    def align(cost):
        return dtw(cost,
                   step_pattern=alignment.stepPattern,
                   window_type=alignment.windowFunction,
                   window_args=window_args,
                   open_begin=alignment.openBegin,
                   open_end=alignment.openEnd,
                   distance_only=not correlation)

    def check_statistic(value, context):
        if numpy.ndim(value) != 0 or not numpy.isfinite(value):
            raise ValueError("%s statistic '%s' is undefined or non-finite; correlation "
                             "requires at least two aligned observations and nonconstant "
                             "aligned series" % (context, statistic))
        return float(value)

    # A distance-only input still contains enough information to recover a path.
    observed = alignment
    if correlation and len(getattr(alignment, "index1", [])) == 0:
        observed = align(lcm)
    est = check_statistic(_compute_statistic(observed, statistic, query, reference),
                          "Observed")

    rng = numpy.random.default_rng(rng)
    permute_query = permute_side in ("query", "both")
    permute_reference = permute_side in ("reference", "both")
    n, m = lcm.shape
    distribution = numpy.empty(R)
    for i in range(R):
        newq = query
        newr = reference
        if permute_what == "values":
            qi = rng.permutation(n) if permute_query else numpy.arange(n)
            ri = rng.permutation(m) if permute_reference else numpy.arange(m)
            plcm = lcm[numpy.ix_(qi, ri)]
            if correlation:
                newq = query[qi, :]
                newr = reference[ri, :]
        else:
            if permute_query:
                newq = _permute_derivative(query, rng)
            if permute_reference:
                newr = _permute_derivative(reference, rng)
            plcm = scipy.spatial.distance.cdist(newq, newr, metric=alignment.distanceMethod)
        pal = align(plcm)
        distribution[i] = check_statistic(_compute_statistic(pal, statistic, newq, newr),
                                          "Permutation %d" % (i + 1))

    # Include ties, with a small tolerance for cumulative-sum roundoff.
    tolerance = 100 * numpy.finfo(float).eps * max(1.0, abs(est))
    p_less = (1 + numpy.sum(distribution <= est + tolerance)) / (R + 1)
    p_greater = (1 + numpy.sum(distribution >= est - tolerance)) / (R + 1)
    if alternative == "less":
        pval = p_less
    elif alternative == "greater":
        pval = p_greater
    else:
        pval = min(1.0, 2 * min(p_less, p_greater))

    return PermutationTestResult({
        'statistic': statistic,
        'estimate': est,
        'p_value': float(pval),
        'replicates': R,
        'alternative': alternative,
        'method': "DTW %s permutation test on %s-side (based on %d permutation rounds)" % (
            permute_what, permute_side, R),
        'null_distribution': distribution if return_distribution else None,
    })
