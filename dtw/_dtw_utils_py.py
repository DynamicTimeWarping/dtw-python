"""Pure Python fallback implementation for :mod:`dtw._dtw_utils`.

This module replicates the behaviour of the Cython extension that powers the
:func:`dtw._globalCostMatrix._globalCostMatrix` helper so that the package
remains importable when the compiled extension is unavailable (for example
when running the test-suite directly from a source checkout before building
artifacts).
"""

from __future__ import annotations

import math
from typing import Any, Dict

import numpy as np

__all__ = ["_computeCM_wrapper"]

# The compiled extension uses INT_MIN as the NA marker for the step matrix.
R_NA_INT = np.iinfo(np.int32).min


def _normalise_dir_matrix(dir_array: np.ndarray, nsteps: int) -> np.ndarray:
    """Return the direction matrix with shape ``(nsteps, 4)``.

    ``step_pattern._get_p()`` yields a 2-D array but callers occasionally pass
    flattened views.  The Cython implementation treats the buffer as a
    Fortran-ordered matrix, therefore we mirror that behaviour and reshape
    accordingly when needed.
    """

    if dir_array.ndim == 2:
        if dir_array.shape[0] == nsteps:
            return dir_array
        if dir_array.shape[1] == nsteps:
            return np.reshape(dir_array, (nsteps, -1), order="F")
    elif dir_array.ndim == 1:
        return np.reshape(dir_array, (nsteps, -1), order="F")

    return np.reshape(dir_array, (nsteps, -1), order="F")


def _computeCM_wrapper(
    wm: np.ndarray,
    lm: np.ndarray,
    nstepsp: np.ndarray,
    dir: np.ndarray,
    cm: np.ndarray,
    sm: np.ndarray | None = None,
) -> Dict[str, Any]:
    """Pure Python drop-in replacement for the Cython wrapper.

    The implementation mirrors :func:`dtw._dtw_utils._computeCM_wrapper` and is
    intentionally written with explicit loops so that the behaviour matches the
    original C routine.
    """

    wm_arr = np.asarray(wm, dtype=np.int32)
    lm_arr = np.asarray(lm, dtype=np.double)
    cm_arr = np.asarray(cm, dtype=np.double)

    if wm_arr.shape != lm_arr.shape or cm_arr.shape != lm_arr.shape:
        raise ValueError("All matrices must share the same shape")

    rows, cols = lm_arr.shape

    nsteps = int(np.asarray(nstepsp, dtype=np.int32).ravel()[0])
    dir_matrix = _normalise_dir_matrix(np.asarray(dir, dtype=np.double), nsteps)
    if dir_matrix.shape[1] != 4:
        raise ValueError("Direction matrix must have four columns")

    pattern_ids = dir_matrix[:, 0].astype(np.int32) - 1
    delta_i = dir_matrix[:, 1].astype(np.int32)
    delta_j = dir_matrix[:, 2].astype(np.int32)
    step_cost = dir_matrix[:, 3]

    npats = (int(pattern_ids.max()) + 1) if nsteps else 0
    clist = np.empty(npats, dtype=np.double)

    if sm is None:
        sm_arr = np.empty_like(lm_arr, dtype=np.int32)
    else:
        sm_arr = np.asarray(sm, dtype=np.int32)
        if sm_arr.shape != lm_arr.shape:
            raise ValueError("Direction matrix must match the local matrix shape")

    sm_arr.fill(R_NA_INT)

    for j in range(rows):
        for i in range(cols):
            if not wm_arr[j, i]:
                continue
            if not math.isnan(cm_arr[j, i]):
                continue

            clist.fill(np.nan)
            for s_idx in range(nsteps):
                p = pattern_ids[s_idx]
                ii = i - delta_i[s_idx]
                jj = j - delta_j[s_idx]
                if ii < 0 or jj < 0:
                    continue

                cost = step_cost[s_idx]
                if cost == -1.0:
                    clist[p] = cm_arr[jj, ii]
                else:
                    clist[p] = clist[p] + cost * lm_arr[jj, ii]

            if npats == 0:
                continue

            valid = ~np.isnan(clist)
            if not np.any(valid):
                continue

            valid_indices = np.nonzero(valid)[0]
            best_local = np.argmin(clist[valid_indices])
            best_index = valid_indices[best_local]
            cm_arr[j, i] = clist[best_index]
            sm_arr[j, i] = best_index + 1

    return {"costMatrix": cm_arr, "directionMatrix": sm_arr}

