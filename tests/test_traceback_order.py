import numpy as np
import pytest

from dtw import asymmetric, dtw, symmetric2, typeIIIc


@pytest.mark.parametrize("pattern", [symmetric2, asymmetric, typeIIIc])
def test_traceback_preserves_expanded_step_order(pattern):
    from dtw import nearOptimalPaths

    costs = np.random.default_rng(42).uniform(size=(7, 8))
    alignment = dtw(costs, step_pattern=pattern, keep_internals=True)
    # The native near-optimal path enumerator reconstructs paths independently.
    reference = nearOptimalPaths(alignment)[0]
    for name in ("index1", "index2", "index1s", "index2s", "stepsTaken"):
        np.testing.assert_array_equal(
            getattr(alignment, name), getattr(reference, name)
        )


@pytest.mark.parametrize("length", [1, 17, 1001])
def test_traceback_long_horizontal_and_vertical_runs(length):
    horizontal = dtw(np.zeros((1, length)))
    vertical = dtw(np.zeros((length, 1)))
    for alignment, row, column in [
        (horizontal, np.zeros(length, dtype=int), np.arange(length)),
        (vertical, np.arange(length), np.zeros(length, dtype=int)),
    ]:
        np.testing.assert_array_equal(alignment.index1, row)
        np.testing.assert_array_equal(alignment.index2, column)
        np.testing.assert_array_equal(alignment.index1s, row)
        np.testing.assert_array_equal(alignment.index2s, column)
        assert len(alignment.stepsTaken) == length - 1
