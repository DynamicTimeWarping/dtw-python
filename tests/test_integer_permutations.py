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
