import numpy as np
import pytest

from dtw import dtw, permutationTest


@pytest.mark.parametrize("dtype", [np.uint8, np.int8, np.int16, np.int64])
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
            floats = [float(value) for value in values]
            if side in (name, "both"):
                increments = [b - a for a, b in zip(floats, floats[1:])]
                permuted = [floats[0]]
                for index in rng.permutation(len(increments)):
                    permuted.append(permuted[-1] + increments[index])
                floats = permuted
            series.append(floats)
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
