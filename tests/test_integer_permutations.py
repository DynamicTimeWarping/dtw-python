import numpy as np
import pytest

from dtw import dtw, permutationTest


@pytest.mark.parametrize("dtype", [np.uint8, np.int8, np.int16,
                                   np.int64, np.uint64])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_integer_increment_permutations(dtype, side):
    bounds = np.iinfo(dtype)
    query = np.array([bounds.max, bounds.min, 0, bounds.max], dtype=dtype)
    reference = np.roll(query, 1)
    alignment = dtw(query, reference, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            integers = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(integers, integers[1:])]
                permuted = [integers[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                integers = permuted
            series.append([float(value) for value in integers])
        expected.append(dtw(*series).distance)
    np.testing.assert_allclose(result.null_distribution, expected)
    tolerance = 100 * np.finfo(float).eps * max(1, abs(result.estimate))
    expected_p = (
        1 + np.count_nonzero(np.array(expected) <= result.estimate + tolerance)
    ) / 20
    assert result.p_value == expected_p


@pytest.mark.parametrize("dtype", [np.complex64, np.complex128])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_complex_increment_permutations(dtype, side):
    query = np.array([1 + 2j, 2 - 1j, 0 + 3j, 4 + 1j], dtype=dtype)
    reference = np.array([1 - 1j, 2 + 1j, 3 + 2j, 2 + 3j], dtype=dtype)

    def metric(a, b):
        return np.linalg.norm(a - b)

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            samples = [complex(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(samples, samples[1:])]
                permuted = [samples[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                samples = permuted
            series.append(samples)
        expected.append(dtw(*series, dist_method=metric).distance)
    np.testing.assert_allclose(result.null_distribution, expected, rtol=1e-6)


@pytest.mark.parametrize("dtype", [np.int64, np.uint64])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_large_integer_constant_increments(dtype, side):
    start = 2**53
    query = np.array([start + i for i in range(4)], dtype=dtype)
    reference = np.full(4, start, dtype=dtype)
    alignment = dtw(query, reference, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    # Both series have constant increments, so permutation changes neither.
    np.testing.assert_array_equal(result.null_distribution,
                                  np.full(19, alignment.distance))
    assert result.p_value == 1


@pytest.mark.parametrize("dtype", [np.int16, np.int64, np.uint64])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_integer_callable_increment_permutations(dtype, side):
    start = 2**53 if dtype != np.int16 else 0
    query = np.array([start + i for i in range(4)], dtype=dtype)
    reference = np.full(4, start, dtype=dtype)

    def metric(a, b):
        assert a.dtype == b.dtype == dtype
        return float(np.bitwise_xor(a, b).sum())

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=9, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    np.testing.assert_array_equal(result.null_distribution,
                                  np.full(9, alignment.distance))
    assert result.p_value == 1


def test_integer_callable_out_of_range_increment_permutations():
    query = np.array([255, 0, 255, 0], dtype=np.uint8)
    reference = np.array([0, 255, 0, 255], dtype=np.uint8)

    def metric(a, b):
        return abs(int(a[0]) - int(b[0]))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side="both",
                             permute_what="increments",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values in (query, reference):
            integers = [int(value) for value in values]
            increments = [b - a for a, b in zip(integers, integers[1:])]
            permuted = [integers[0]]
            for index in rng.permutation(len(increments)):
                permuted.append(permuted[-1] + increments[index])
            series.append(np.array(permuted, dtype=object))
        expected.append(dtw(*series, dist_method=metric).distance)
    np.testing.assert_array_equal(result.null_distribution, expected)


@pytest.mark.parametrize("side", ["query", "reference", "both"])
@pytest.mark.parametrize("statistic", ["pearson", "spearman", "kendall"])
def test_integer_callable_out_of_range_correlations(side, statistic):
    query = np.array([255, 0, 255, 0], dtype=np.uint8)
    reference = np.array([0, 255, 0, 255], dtype=np.uint8)

    def metric(a, b):
        return abs(int(a[0]) - int(b[0]))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments", statistic=statistic,
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    from scipy import stats
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            integers = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(integers, integers[1:])]
                permuted = [integers[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                integers = permuted
            series.append(np.array(integers, dtype=object))
        warped = dtw(*series, dist_method=metric)
        q = np.array(series[0][warped.index1], dtype=float)
        r = np.array(series[1][warped.index2], dtype=float)
        expected.append(
            getattr(stats, statistic + "r")(q, r)[0] if statistic != "kendall"
            else stats.kendalltau(q, r)[0])
    np.testing.assert_allclose(result.null_distribution, expected, atol=1e-15)


@pytest.mark.parametrize("dtype", [np.uint8, np.int8, np.uint16, np.int16])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_integer_callable_numeric_ufunc(dtype, side):
    limits = np.iinfo(dtype)
    query = np.array([limits.max, limits.min, limits.max, limits.min],
                     dtype=dtype)
    reference = query[::-1].copy()

    def metric(a, b):
        return np.abs(np.sin(a, dtype=np.float64)
                      - np.sin(b, dtype=np.float64)).sum()

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            integers = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(integers, integers[1:])]
                permuted = [integers[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                integers = permuted
            series.append(np.array(integers, dtype=np.int64))
        expected.append(dtw(*series, dist_method=metric).distance)
    np.testing.assert_allclose(result.null_distribution, expected, atol=1e-15)


def test_integer_walk_beyond_native_range():
    from dtw.permutationTest import _permute_derivative

    limit = np.iinfo(np.uint64).max
    query = np.array([[limit], [0], [limit], [0]], dtype=np.uint64)

    class Reordered:
        def permutation(self, size):
            assert size == 3
            return np.array([1, 0, 2])

    result = _permute_derivative(query, Reordered(), keep_integer=True)
    assert result.dtype == object
    assert result[:, 0].tolist() == [limit, 2 * int(limit), limit, 0]


@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_uint64_callable_widened_pair(side):
    start = 2**53 + 1
    query = np.array([start, 0, start, 0], dtype=np.uint64)
    reference = np.array([0, start, 0, start], dtype=np.uint64)

    def metric(a, b):
        return np.count_nonzero(np.bitwise_xor(a, b))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            integers = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(integers, integers[1:])]
                out = [integers[0]]
                for index in rng.permutation(len(increments)):
                    out.append(out[-1] + increments[index])
                integers = out
            series.append(integers)
        cost = [[float(a != b) for b in series[1]] for a in series[0]]
        expected.append(dtw(np.array(cost)).distance)
    np.testing.assert_array_equal(result.null_distribution, expected)


def test_signed_callable_beyond_int64_stays_signed():
    limit = np.iinfo(np.int64).max
    query = np.array([limit, 1, limit, 0], dtype=np.int64)
    reference = np.array([limit, 0, limit, 0], dtype=np.int64)

    def metric(a, b):
        return np.abs(a - b).sum()

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True,
                    window_type="sakoechiba", window_args={"window_size": 0})
    result = permutationTest(alignment, R=1, permute_side="both",
                             permute_what="increments",
                             return_distribution=True, rng=11)
    # Seed 11 permutes both increment sequences in order [1, 0, 2]. The two
    # reconstructed walks differ by one at the first interior point. symmetric2
    # weights that diagonal cost by two.
    np.testing.assert_array_equal(result.null_distribution, [2.0])


def test_unsigned_callable_pair_can_use_uint64():
    query = np.array([255, 0, 255, 0], dtype=np.uint8)
    reference = np.full(4, 2**63 + 1, dtype=np.uint64)

    def metric(a, b):
        return np.abs(np.sin(a, dtype=np.float64)
                      - np.sin(b, dtype=np.float64)).sum()

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=1, permute_side="query",
                             permute_what="increments",
                             return_distribution=True, rng=11)
    # The widened positive query and the held unsigned reference jointly fit
    # uint64, allowing numeric ufuncs that cannot operate on objects.
    expected = dtw(np.array([255, 510, 255, 0], dtype=np.uint64), reference,
                   dist_method=metric).distance
    np.testing.assert_array_equal(result.null_distribution, [expected])


@pytest.mark.parametrize("dtype", [np.int64, np.uint64])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
@pytest.mark.parametrize("statistic", ["spearman", "kendall"])
def test_named_metric_preserves_exact_integer_ranks(dtype, side, statistic):
    query = np.array([2**53, 2**53 + 1, 2**53 + 2], dtype=dtype)
    alignment = dtw(query, query, keep_internals=True,
                    window_type="sakoechiba", window_args={"window_size": 0})
    result = permutationTest(alignment, R=7, permute_side=side,
                             permute_what="increments", statistic=statistic,
                             return_distribution=True, rng=11)
    np.testing.assert_allclose(result.null_distribution, 1, rtol=0, atol=1e-15)
    assert result.p_value == 1


@pytest.mark.parametrize("dtypes", [
    (np.int8, np.int16), (np.int16, np.int8),
    (np.uint8, np.uint16), (np.uint16, np.uint8)])
@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_callable_preserves_unchanged_mixed_integer_dtypes(dtypes, side):
    query = np.arange(4, dtype=dtypes[0])
    reference = np.arange(4, dtype=dtypes[1])

    def metric(a, b):
        assert a.dtype == dtypes[0]
        assert b.dtype == dtypes[1]
        return sum(abs(int(x) - int(y)) for x, y in zip(a, b))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=7, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=11)
    np.testing.assert_array_equal(result.null_distribution, np.zeros(7))
    assert result.p_value == 1


@pytest.mark.parametrize("reference_dtype", [np.int16, np.uint16])
def test_callable_preserves_compatible_held_reference(reference_dtype):
    query = np.array([255, 0, 255, 0], dtype=np.uint8)
    reference = np.array([0, 255, 0, 255], dtype=reference_dtype)

    def metric(a, b):
        assert b.dtype == reference_dtype
        return np.count_nonzero(np.bitwise_xor(a, b))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side="query",
                             permute_what="increments",
                             return_distribution=True, rng=17)
    expected = []
    rng = np.random.default_rng(17)
    for _ in range(19):
        out = [255]
        for i in rng.permutation(3):
            out.append(out[-1] + [-255, 255, -255][i])
        cost = [[float(a != int(b)) for b in reference] for a in out]
        expected.append(dtw(np.array(cost)).distance)
    np.testing.assert_array_equal(result.null_distribution, expected)


@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_kendall_walk_beyond_native_integer_range(side):
    limit = int(np.iinfo(np.uint64).max)
    query = np.array([limit, 0, limit, 0], dtype=np.uint64)
    reference = np.arange(4, dtype=np.uint64)

    def metric(a, b):
        return abs(int(a[0]) - int(b[0]))

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True,
                    window_type="sakoechiba", window_args={"window_size": 0})
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments", statistic="kendall",
                             return_distribution=True, rng=11)
    expected = []
    rng = np.random.default_rng(11)
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            out = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(out, out[1:])]
                out = [out[0]]
                for i in rng.permutation(len(increments)):
                    out.append(out[-1] + increments[i])
            series.append(out)
        score, non_tied_q, non_tied_r = 0, 0, 0
        for i in range(4):
            for j in range(i):
                qi, qj = series[0][i], series[0][j]
                ri, rj = series[1][i], series[1][j]
                q = (qi > qj) - (qi < qj)
                r = (ri > rj) - (ri < rj)
                score += q * r
                non_tied_q += q != 0
                non_tied_r += r != 0
        expected.append(score / np.sqrt(non_tied_q * non_tied_r))
    np.testing.assert_allclose(result.null_distribution, expected,
                               rtol=0, atol=1e-15)


@pytest.mark.parametrize("dtype", [
    np.float32, np.float64, np.complex64, np.complex128])
@pytest.mark.parametrize("integer_side", ["query", "reference"])
def test_callable_mixed_inexact_beyond_integer_range(dtype, integer_side):
    limit = int(np.iinfo(np.uint64).max)
    integer = np.array([limit, 0, limit, 0], dtype=np.uint64)
    inexact = np.arange(4).astype(dtype)
    if np.issubdtype(dtype, np.complexfloating):
        inexact += 0.25j

    def metric(a, b):
        return np.abs(np.sin(a - b)).sum()

    series = ([integer, inexact] if integer_side == "query"
              else [inexact, integer])
    alignment = dtw(*series, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=1, permute_side=integer_side,
                             permute_what="increments",
                             return_distribution=True, rng=11)
    # Match the original pair's inexact arithmetic promotion. Retained exact
    # samples for correlation statistics are independent of these cost inputs.
    promoted = np.result_type(integer.dtype, inexact.dtype)
    widened = np.array([limit, 2 * limit, limit, 0], dtype=promoted)
    expected_series = ([widened, inexact] if integer_side == "query"
                       else [inexact, widened])
    expected = dtw(*expected_series, dist_method=metric).distance
    np.testing.assert_array_equal(result.null_distribution, [expected])


@pytest.mark.parametrize("dtype", [np.int64, np.uint64])
def test_pearson_preserves_narrow_out_of_range_walk(dtype):
    limit = int(np.iinfo(dtype).max)
    offsets = list(range(1026)) + list(range(1024, -1, -1))
    query = np.array([limit - x for x in offsets], dtype=dtype)
    alignment = dtw(query, query, keep_internals=True,
                    window_type="sakoechiba", window_args={"window_size": 0})
    result = permutationTest(alignment, R=1, permute_side="query",
                             permute_what="increments", statistic="pearson",
                             return_distribution=True, rng=11)
    increments = [a - b for a, b in zip(offsets, offsets[1:])]
    centered = [0]
    for i in np.random.default_rng(11).permutation(len(increments)):
        centered.append(centered[-1] + increments[i])
    expected = np.corrcoef(centered, [-x for x in offsets])[0, 1]
    np.testing.assert_allclose(result.null_distribution, [expected],
                               rtol=0, atol=1e-15)


@pytest.mark.parametrize("side", ["query", "reference"])
def test_object_safe_mixed_callable_keeps_integer_low_bits(side):
    limit = int(np.iinfo(np.uint64).max)
    integer = np.array([limit, 0, limit, 0], dtype=np.uint64)
    floating = np.arange(4, dtype=float)

    def metric(a, b):
        return float((int(a[0]) ^ int(b[0])) & 1)

    series = [integer, floating] if side == "query" else [floating, integer]
    alignment = dtw(*series, dist_method=metric, keep_internals=True,
                    window_type="sakoechiba", window_args={"window_size": 0})
    result = permutationTest(alignment, R=1, permute_side=side,
                             permute_what="increments",
                             return_distribution=True, rng=11)
    # max, 2*max, max, 0 have odd/even/odd/even parity. Every diagonal
    # mismatch costs one; symmetric2 uses weights 1, 2, 2, 2.
    np.testing.assert_array_equal(result.null_distribution, [7.0])


def test_mixed_callable_application_type_error_is_not_retried():
    limit = np.iinfo(np.uint64).max

    def metric(a, b):
        if a.dtype == object:
            raise TypeError("custom application error")
        return np.abs(np.sin(a - b)).sum()

    alignment = dtw(np.array([limit, 0, limit, 0], dtype=np.uint64),
                    np.arange(4, dtype=float), dist_method=metric,
                    keep_internals=True)
    with pytest.raises(TypeError, match="custom application error"):
        permutationTest(alignment, R=1, permute_side="query",
                        permute_what="increments", rng=11)


def test_mixed_callable_preserves_scipy_metric_keywords():
    from scipy.spatial.distance import mahalanobis

    limit = int(np.iinfo(np.uint64).max)
    query = np.array([limit, 0, limit, 0], dtype=np.uint64)
    reference = np.arange(4, dtype=float)
    alignment = dtw(query, reference, dist_method=mahalanobis,
                    keep_internals=True)
    result = permutationTest(alignment, R=1, permute_side="query",
                             permute_what="increments",
                             return_distribution=True, rng=11)
    widened = np.array([limit, 2 * limit, limit, 0], dtype=float)
    expected = dtw(widened, reference, dist_method=mahalanobis).distance
    np.testing.assert_allclose(result.null_distribution, [expected])


@pytest.mark.parametrize("side", ["query", "reference", "both"])
def test_exact_out_of_range_spearman_ranks(side):
    from scipy import stats

    limit = np.iinfo(np.int64).max
    query = np.array([limit - 1, limit, limit - 1, limit], dtype=np.int64)
    reference = query[::-1].copy()

    def metric(a, b):
        return abs(int(a[0]) - int(b[0]))

    def exact_ranks(values):
        # Independent pairwise ordinal counts, avoiding any floating cast.
        return [1 + sum(y < x for y in values)
                + (sum(y == x for y in values) - 1) / 2 for x in values]

    alignment = dtw(query, reference, dist_method=metric, keep_internals=True)
    result = permutationTest(alignment, R=19, permute_side=side,
                             permute_what="increments", statistic="spearman",
                             return_distribution=True, rng=17)
    rng = np.random.default_rng(17)
    expected = []
    for _ in range(19):
        series = []
        for values, name in [(query, "query"), (reference, "reference")]:
            integers = [int(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(integers, integers[1:])]
                permuted = [integers[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                integers = permuted
            series.append(np.array(integers, dtype=object))
        warped = dtw(*series, dist_method=metric)
        q = exact_ranks(series[0][warped.index1].tolist())
        r = exact_ranks(series[1][warped.index2].tolist())
        expected.append(stats.spearmanr(q, r)[0])
    np.testing.assert_allclose(result.null_distribution, expected, atol=1e-15)
