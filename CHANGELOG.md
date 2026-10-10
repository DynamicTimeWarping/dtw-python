Changelog
=========


(unreleased)
------------
- Port R dtw 2.1 features: nearOptimalPaths, permutationTest, dtwDist.
  [Claude Opus 5.5, Toni]

  New functions, following the R package:

  * nearOptimalPaths() lists all warping paths within a cost threshold
    (Waterman and Byers, 1985). The search is in Cython, mirroring R's
    dtw_kbest.c; paths are returned as DTW objects.
  * permutationTest() compares a DTW statistic with value or increment
    permutations of the query/reference. Uses rng= for reproducibility
    and returns a PermutationTestResult.
  * dtwDist() computes DTW dissimilarity matrices.
  * dtwWindow_plot() visualizes a windowing function.

  Fixes, matching R 2.1:

  * With open_begin, the window is evaluated on the query's own indices
    instead of the padded matrix, which shifted it by one row. Results
    change for windowed open-begin alignments.
  * countPaths() no longer counts open-begin paths starting outside the
    window.
  * Open-end alignments with no valid path raise a clear error instead of
    numpy's "All-NaN slice".

  dtw() now stores distanceMethod, needed for increment permutations.


v1.9.0 (2026-10-08)
-------------------
- Test free-threaded Python and concurrent alignments. [Claude Opus 5.5,
  Toni]

  - tests/test_threads.py: on free-threaded builds, check that importing
    dtw leaves the GIL disabled (fails on 1.8.1, whose extension did not
    declare free-threading compatibility)
  - tests/test_threads.py: run 24 alignments with three step patterns on
    8 threads and check distances, warping paths and cost matrices match
    a serial run
  - quick_test_and_codecov.yml: add 3.14t to the uv test matrix
- Maintainer maintenance. [Toni]
- Modernize Cython build and guard the C core wrapper. [Claude Opus 5.5,
  Toni]

  - _dtw_utils.pyx: drop unused `cimport numpy` (and `import warnings`);
    the extension no longer uses the NumPy C API
  - _dtw_utils.pyx: run computeCM without the GIL (`noexcept nogil`,
    `with nogil:`) and declare `freethreading_compatible=True`
  - _dtw_utils.pyx: check that window, local cost and cost matrices have
    the same shape, and that the step pattern is well formed (description
    length 4*nsteps, integer pattern numbers from 1, ascending); raise
    ValueError instead of reading out of bounds or exit()ing in dtw_core.c
  - setup.py: plain Extension with the .pyx source, cythonized by
    setuptools; remove cythonize(force=True), numpy include, and metadata
    duplicated in pyproject (name, packages, url, version, zip_safe)
  - pyproject.toml: build requires setuptools>=77 (SPDX license string)
    and Cython>=3.1; drop numpy and wheel from build requirements
  - pyproject.toml: read version from dtw.__version__; exclude .c/.h/.pyx
    sources from wheels
  - MANIFEST.in: keep the generated dtw/_dtw_utils.c out of the sdist
  - .bumpversion.toml: stop bumping setup.py, which no longer has a version
  - tests/test_wrapper_checks.py: tests for the new input checks
- Merge pull request #158 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-4.3.0.
  [Toni Giorgino]

  Bump pypa/cibuildwheel from 4.2.1 to 4.3.0
- Bump pypa/cibuildwheel from 4.2.1 to 4.3.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 4.2.1 to 4.3.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v4.2.1...v4.3.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 4.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...


v1.8.1 (2026-10-06)
-------------------
- Remove matplotlib test-time dep. [Toni]


v1.8.0 (2026-10-06)
-------------------
- New python versions. [Toni]
- Accept 1-D vectors in dtwPlotTwoWay. [Claude Opus 5.5, Toni]

  Reshape 1-D timeseries into columns before checking their shape.
- Accept local cost matrices of any numeric dtype and memory layout.
  [Claude Opus 5.5, Toni]

  The Cython wrapper requires C-contiguous doubles; convert the input
  with ascontiguousarray instead of numpy.array.
- Accept unique abbreviations of window type names. [Claude Opus 5.5,
  Toni]

  The documentation states that abbreviations are allowed, as in R's
  match.arg, but they were not supported.
- Raise ValueError for unknown window, step pattern and R-J type names.
  [Claude Opus 5.5, Toni]

  The .get(key, lambda: _error(...)) fallback returned the lambda instead
  of calling it, producing a confusing TypeError later. Also reject step
  pattern names that are not StepPattern objects (e.g. "numpy").
- Fix crash with open_begin=True and distance_only=True. [Claude Opus
  5.5, Toni]

  Path trimming accessed index attributes that are not computed when
  backtracking is skipped. Only trim the path when it exists.
- Fix off-by-one in itakuraWindow. [Claude Opus 5.5, Toni]

  The R inequalities were copied verbatim although R indices are 1-based,
  excluding the origin and differing from R's window. Translate them to
  0-based indices; the window now matches R exactly.
- Fix slantedBandWindow not reaching the end corner. [Claude Opus 5.5,
  Toni]

  The 1-based R formula iw*M/N was kept with 0-based indices, so the
  diagonal ended at (N-1)*M/N instead of M-1 and narrow bands excluded
  the corner. Make the diagonal run corner to corner, as documented.
- Fix warpArea() not averaging duplicate query indices. [Claude Opus
  5.5, Toni]

  Reuse the tie-averaging interpolation from warp.py instead of calling
  interp1d on duplicated x values. The result now matches R (6 for the
  documented example), so the doctest is re-enabled.
- Fix warp() producing invalid indices when the path skips samples.
  [Claude Opus 5.5, Toni]

  Empty bins in _solveTies() caused 0/0 = NaN, which interp1d propagated
  and which was then cast to garbage integers. Average ties only over
  indices that occur and interpolate with numpy.interp, clamping leading
  out-of-range points to the first value.
- Merge pull request #157 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-4.2.1.
  [Toni Giorgino]

  Bump pypa/cibuildwheel from 4.1.0 to 4.2.1
- Bump pypa/cibuildwheel from 4.1.0 to 4.2.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 4.1.0 to 4.2.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v4.1.0...v4.2.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 4.2.1
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #154 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.14.2. [Toni Giorgino]

  Bump pypa/gh-action-pypi-publish from 1.14.1 to 1.14.2
- Bump pypa/gh-action-pypi-publish from 1.14.1 to 1.14.2.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.14.1 to 1.14.2.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.14.1...v1.14.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-version: 1.14.2
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #149 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-4.1.0.
  [Toni Giorgino]

  Bump pypa/cibuildwheel from 4.0.0 to 4.1.0
- Bump pypa/cibuildwheel from 4.0.0 to 4.1.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 4.0.0 to 4.1.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v4.0.0...v4.1.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 4.1.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #151 from
  DynamicTimeWarping/dependabot/github_actions/actions/setup-python-7.
  [Toni Giorgino]

  Bump actions/setup-python from 6 to 7
- Bump actions/setup-python from 6 to 7. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 6 to 7.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v6...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #152 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.14.1. [Toni Giorgino]

  Bump pypa/gh-action-pypi-publish from 1.14.0 to 1.14.1
- Bump pypa/gh-action-pypi-publish from 1.14.0 to 1.14.1.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.14.0 to 1.14.1.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.14.0...v1.14.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-version: 1.14.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #150 from
  DynamicTimeWarping/dependabot/github_actions/actions/checkout-7. [Toni
  Giorgino]

  Bump actions/checkout from 6 to 7
- Bump actions/checkout from 6 to 7. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 6 to 7.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v6...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...


v1.7.5 (2026-06-12)
-------------------
- Remove tests from wheel. [Toni]
- Merge pull request #148 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-4.0.0.
  [Toni G]

  Bump pypa/cibuildwheel from 3.4.1 to 4.0.0
- Bump pypa/cibuildwheel from 3.4.1 to 4.0.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.4.1 to 4.0.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.4.1...v4.0.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 4.0.0
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #147 from
  DynamicTimeWarping/dependabot/github_actions/codecov/codecov-action-7.
  [Toni G]

  Bump codecov/codecov-action from 6 to 7
- Bump codecov/codecov-action from 6 to 7. [dependabot[bot]]

  Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 6 to 7.
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v6...v7)

  ---
  updated-dependencies:
  - dependency-name: codecov/codecov-action
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Add multivariate alignment example to documentation. [Toni]
- Fix typos in documentation and add missing example. [Toni]
- Add context7.json with URL and public key. [Toni G]
- Merge pull request #146 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.14.0. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.13.0 to 1.14.0
- Bump pypa/gh-action-pypi-publish from 1.13.0 to 1.14.0.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.13.0 to 1.14.0.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.13.0...v1.14.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-version: 1.14.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #144 from
  DynamicTimeWarping/dependabot/github_actions/codecov/codecov-action-6.
  [Toni G]

  Bump codecov/codecov-action from 5 to 6
- Bump codecov/codecov-action from 5 to 6. [dependabot[bot]]

  Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 5 to 6.
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: codecov/codecov-action
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #145 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.4.1.
  [Toni G]

  Bump pypa/cibuildwheel from 3.4.0 to 3.4.1
- Bump pypa/cibuildwheel from 3.4.0 to 3.4.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.4.0 to 3.4.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.4.0...v3.4.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.4.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Fix countpaths. [Toni]
- Skip warparea test. [Toni]
- Cosmetic tweaks + rm agents. [Toni]
- Merge pull request #143 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.4.0.
  [Toni G]

  Bump pypa/cibuildwheel from 3.3.1 to 3.4.0
- Bump pypa/cibuildwheel from 3.3.1 to 3.4.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.3.1 to 3.4.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.3.1...v3.4.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.4.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #142 from
  DynamicTimeWarping/dependabot/github_actions/actions/download-
  artifact-8. [Toni G]

  Bump actions/download-artifact from 7 to 8
- Bump actions/download-artifact from 7 to 8. [dependabot[bot]]

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 7 to 8.
  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v7...v8)

  ---
  updated-dependencies:
  - dependency-name: actions/download-artifact
    dependency-version: '8'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #141 from
  DynamicTimeWarping/dependabot/github_actions/actions/upload-
  artifact-7. [Toni G]

  Bump actions/upload-artifact from 6 to 7
- Bump actions/upload-artifact from 6 to 7. [dependabot[bot]]

  Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 6 to 7.
  - [Release notes](https://github.com/actions/upload-artifact/releases)
  - [Commits](https://github.com/actions/upload-artifact/compare/v6...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/upload-artifact
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Documenting roxypick. [Toni]
- Uv build test. [Toni]
- Disable wheels temporarily. [Toni]
- Don't test 3.15. [Toni]
- Matrix of pythons. [Toni]
- Rationalize actions. [Toni]
- Make the expensive build only run on release. add quick uv test.
  [Toni]
- Remove obsolete universal wheels. [Toni]
- Migrate to bump-my-version. [Toni]
- Ruff tests. [Toni]
- Fix warning on step pattern plot. [Toni]


v1.7.4 (2026-02-03)
-------------------
- Rm win plat. [Toni]
- Merge pull request #138 from
  DynamicTimeWarping/dependabot/github_actions/actions/download-
  artifact-7. [Toni G]

  Bump actions/download-artifact from 6 to 7
- Bump actions/download-artifact from 6 to 7. [dependabot[bot]]

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 6 to 7.
  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v6...v7)

  ---
  updated-dependencies:
  - dependency-name: actions/download-artifact
    dependency-version: '7'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #137 from
  DynamicTimeWarping/dependabot/github_actions/actions/upload-
  artifact-6. [Toni G]

  Bump actions/upload-artifact from 5 to 6
- Bump actions/upload-artifact from 5 to 6. [dependabot[bot]]

  Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 5 to 6.
  - [Release notes](https://github.com/actions/upload-artifact/releases)
  - [Commits](https://github.com/actions/upload-artifact/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/upload-artifact
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Update platforms. [Toni]


v1.7.3 (2026-02-03)
-------------------
- Add plots group, remove test one. [Toni]
- Skip if matplotlib  missing. [Toni]
- Add test for two-way plot to reject multivariate time series. [Toni]
- Fix https://github.com/DynamicTimeWarping/dtw-python/issues/140.
  [Toni]
- Add tests for plot two way. [Toni]
- Merge pull request #136 from
  DynamicTimeWarping/dependabot/github_actions/actions/checkout-6. [Toni
  G]

  Bump actions/checkout from 5 to 6
- Bump actions/checkout from 5 to 6. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 5 to 6.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #135 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.3.0.
  [Toni G]

  Bump pypa/cibuildwheel from 3.2.1 to 3.3.0
- Bump pypa/cibuildwheel from 3.2.1 to 3.3.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.2.1 to 3.3.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.2.1...v3.3.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.3.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #134 from
  DynamicTimeWarping/dependabot/github_actions/actions/upload-
  artifact-5. [Toni G]

  Bump actions/upload-artifact from 4 to 5
- Bump actions/upload-artifact from 4 to 5. [dependabot[bot]]

  Bumps [actions/upload-artifact](https://github.com/actions/upload-artifact) from 4 to 5.
  - [Release notes](https://github.com/actions/upload-artifact/releases)
  - [Commits](https://github.com/actions/upload-artifact/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/upload-artifact
    dependency-version: '5'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #133 from
  DynamicTimeWarping/dependabot/github_actions/actions/download-
  artifact-6. [Toni G]

  Bump actions/download-artifact from 5 to 6
- Bump actions/download-artifact from 5 to 6. [dependabot[bot]]

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 5 to 6.
  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/download-artifact
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #132 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.2.1.
  [Toni G]

  Bump pypa/cibuildwheel from 3.2.0 to 3.2.1
- Bump pypa/cibuildwheel from 3.2.0 to 3.2.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.2.0 to 3.2.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.2.0...v3.2.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.2.1
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...


v1.7.2 (2025-10-06)
-------------------
- Last before bumpversion. [Toni]


v1.7.1 (2025-10-06)
-------------------
- Last before bumpversion. [Toni]


v1.6.0 (2025-10-06)
-------------------
- Uv bump2version. [Toni]
- Add version to cli. [Toni]
- Drop obsolete python. [Toni]
- Codex UV fix. [Toni]
- Fix license warnings. [Toni]
- Remove numpy RC . remove importlib pytest. [Toni]
- Switch to uv. [Toni]
- Merge pull request #128 from
  DynamicTimeWarping/dependabot/github_actions/actions/setup-python-6.
  [Toni G]

  Bump actions/setup-python from 5 to 6
- Bump actions/setup-python from 5 to 6. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 5 to 6.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v5...v6)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-version: '6'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #129 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.2.0.
  [Toni G]

  Bump pypa/cibuildwheel from 3.1.4 to 3.2.0
- Bump pypa/cibuildwheel from 3.1.4 to 3.2.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.1.4 to 3.2.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.1.4...v3.2.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.2.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #127 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.13.0. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0
- Bump pypa/gh-action-pypi-publish from 1.12.4 to 1.13.0.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.12.4 to 1.13.0.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.12.4...v1.13.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-version: 1.13.0
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #126 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.1.4.
  [Toni G]

  Bump pypa/cibuildwheel from 3.0.1 to 3.1.4
- Bump pypa/cibuildwheel from 3.0.1 to 3.1.4. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 3.0.1 to 3.1.4.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v3.0.1...v3.1.4)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.1.4
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #125 from
  DynamicTimeWarping/dependabot/github_actions/actions/checkout-5. [Toni
  G]

  Bump actions/checkout from 4 to 5
- Bump actions/checkout from 4 to 5. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 4 to 5.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-version: '5'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #124 from
  DynamicTimeWarping/dependabot/github_actions/actions/download-
  artifact-5. [Toni G]

  Bump actions/download-artifact from 4 to 5
- Bump actions/download-artifact from 4 to 5. [dependabot[bot]]

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 4 to 5.
  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/download-artifact
    dependency-version: '5'
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Remove obsolete build targets cp36* pp* [Toni G]
- Merge pull request #119 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-3.0.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.23.2 to 3.0.1
- Bump pypa/cibuildwheel from 2.23.2 to 3.0.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.23.2 to 3.0.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.23.2...v3.0.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-version: 3.0.1
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #116 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.23.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.23.1 to 2.23.2
- Bump pypa/cibuildwheel from 2.23.1 to 2.23.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.23.1 to 2.23.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.23.1...v2.23.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Update codecov.yml. [Toni G]
- Merge pull request #113 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.12.4. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.12.3 to 1.12.4
- Bump pypa/gh-action-pypi-publish from 1.12.3 to 1.12.4.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.12.3 to 1.12.4.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.12.3...v1.12.4)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #115 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.23.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.22.0 to 2.23.1
- Bump pypa/cibuildwheel from 2.22.0 to 2.23.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.22.0 to 2.23.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/v2.23.1/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.22.0...v2.23.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Sync with R. [Toni]
- Merge pull request #110 from
  DynamicTimeWarping/dependabot/github_actions/codecov/codecov-action-5.
  [Toni G]

  Bump codecov/codecov-action from 4 to 5
- Bump codecov/codecov-action from 4 to 5. [dependabot[bot]]

  Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 4 to 5.
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: codecov/codecov-action
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #111 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.22.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.21.3 to 2.22.0
- Bump pypa/cibuildwheel from 2.21.3 to 2.22.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.21.3 to 2.22.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.21.3...v2.22.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #112 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.12.3. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.11.0 to 1.12.3
- Bump pypa/gh-action-pypi-publish from 1.11.0 to 1.12.3.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.11.0 to 1.12.3.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.11.0...v1.12.3)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #106 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.21.3.
  [Toni G]

  Bump pypa/cibuildwheel from 2.21.2 to 2.21.3
- Bump pypa/cibuildwheel from 2.21.2 to 2.21.3. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.21.2 to 2.21.3.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.21.2...v2.21.3)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #107 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.11.0. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.10.3 to 1.11.0
- Bump pypa/gh-action-pypi-publish from 1.10.3 to 1.11.0.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.10.3 to 1.11.0.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.10.3...v1.11.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #105 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.10.3. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.10.2 to 1.10.3
- Bump pypa/gh-action-pypi-publish from 1.10.2 to 1.10.3.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.10.2 to 1.10.3.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.10.2...v1.10.3)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #104 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.21.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.21.1 to 2.21.2
- Bump pypa/cibuildwheel from 2.21.1 to 2.21.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.21.1 to 2.21.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.21.1...v2.21.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #103 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.10.2. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.10.1 to 1.10.2
- Bump pypa/gh-action-pypi-publish from 1.10.1 to 1.10.2.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.10.1 to 1.10.2.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.10.1...v1.10.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #102 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.21.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.20.0 to 2.21.1
- Bump pypa/cibuildwheel from 2.20.0 to 2.21.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.20.0 to 2.21.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.20.0...v2.21.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #100 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.10.1. [dependabot[bot]]
- Bump pypa/gh-action-pypi-publish from 1.10.0 to 1.10.1.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.10.0 to 1.10.1.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.10.0...v1.10.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Update release instruc. [Toni]


v1.5.3 (2024-09-02)
-------------------
- Merge pull request #99 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.10.0. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.9.0 to 1.10.0
- Bump pypa/gh-action-pypi-publish from 1.9.0 to 1.10.0.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.9.0 to 1.10.0.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.9.0...v1.10.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #98 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.20.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.19.2 to 2.20.0
- Bump pypa/cibuildwheel from 2.19.2 to 2.20.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.19.2 to 2.20.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.19.2...v2.20.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...


v1.5.2 (2024-09-02)
-------------------
- Doctest failure. [Toni]
- Maintenance. [Toni]
- Merge pull request #97 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.19.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.19.1 to 2.19.2
- Bump pypa/cibuildwheel from 2.19.1 to 2.19.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.19.1 to 2.19.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.19.1...v2.19.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #96 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.9.0. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.8.14 to 1.9.0
- Bump pypa/gh-action-pypi-publish from 1.8.14 to 1.9.0.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.8.14 to 1.9.0.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.8.14...v1.9.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #95 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.19.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.19.0 to 2.19.1
- Bump pypa/cibuildwheel from 2.19.0 to 2.19.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.19.0 to 2.19.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.19.0...v2.19.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #94 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.19.0.
  [dependabot[bot]]
- Bump pypa/cibuildwheel from 2.18.1 to 2.19.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.18.1 to 2.19.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.18.1...v2.19.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Update _dtw_utils.pyx, no import array. [Toni G]

  Should make it work with pypy


v1.5.1 (2024-05-27)
-------------------
- Indent. [Toni]
- Cython. [Toni]
- Changelog. [Toni]


v1.5.0 (2024-05-23)
-------------------
- Modernize build and    attempt to numpy 2. [Toni]
- Merge pull request #93 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.18.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.17.0 to 2.18.1
- --- updated-dependencies: - dependency-name: pypa/cibuildwheel
  dependency-type: direct:production   update-type: version-
  update:semver-minor ... [dependabot[bot]]
- No inh diag. [Toni]


v1.4.4 (2024-05-18)
-------------------
- Update cython 3. [Toni]


v1.4.3 (2024-05-18)
-------------------
- Fix test for numpy2. [Toni]
- List new Python versions. [Toni]


v1.4.2 (2024-03-19)
-------------------
- Changelog. [Toni]
- Update build_wheels.yml. [Toni G]


v1.4.1 (2024-03-18)
-------------------
- Update build_wheels.yml. [Toni G]
- Update build_wheels.yml. [Toni G]

  concurrency
- Update build_wheels.yml. [Toni G]

  cancel-in-progress: true
- Update build_wheels.yml. [Toni G]

  fix artifact name?
- Update build_wheels.yml. [Toni G]
- Merge pull request #88 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.8.14. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.8.11 to 1.8.14
- Bump pypa/gh-action-pypi-publish from 1.8.11 to 1.8.14.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.8.11 to 1.8.14.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.8.11...v1.8.14)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #89 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.17.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.16.5 to 2.17.0
- Bump pypa/cibuildwheel from 2.16.5 to 2.17.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.16.5 to 2.17.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.16.5...v2.17.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Delete .github/ISSUE_TEMPLATE.md. [Toni G]
- Update issue templates. [Toni G]


v1.4.0 (2024-03-18)
-------------------
- Fix off-by-one in warp. [Toni]
- Merge pull request #85 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.16.5.
  [Toni G]

  Bump pypa/cibuildwheel from 2.16.2 to 2.16.5
- Bump pypa/cibuildwheel from 2.16.2 to 2.16.5. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.16.2 to 2.16.5.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.16.2...v2.16.5)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Squashed commit of the following: [Toni]

  commit 7a3b4fd2689e0652b21d16469ae6406ba66125c3
- Use trusted PyPI uploads. [Toni G]
- Update build_wheels.yml. [Toni G]


v1.3.1 (2023-12-20)
-------------------
- Fix transpose. [Toni]
- Merge pull request #80 from
  DynamicTimeWarping/dependabot/github_actions/actions/download-
  artifact-4. [Toni G]

  Bump actions/download-artifact from 3 to 4
- Bump actions/download-artifact from 3 to 4. [dependabot[bot]]

  Bumps [actions/download-artifact](https://github.com/actions/download-artifact) from 3 to 4.
  - [Release notes](https://github.com/actions/download-artifact/releases)
  - [Commits](https://github.com/actions/download-artifact/compare/v3...v4)

  ---
  updated-dependencies:
  - dependency-name: actions/download-artifact
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #79 from
  DynamicTimeWarping/dependabot/github_actions/actions/setup-python-5.
  [Toni G]

  Bump actions/setup-python from 4 to 5
- Bump actions/setup-python from 4 to 5. [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 4 to 5.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v4...v5)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #75 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.16.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.16.0 to 2.16.2
- Bump pypa/cibuildwheel from 2.16.0 to 2.16.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.16.0 to 2.16.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.16.0...v2.16.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #78 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.8.11. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.8.10 to 1.8.11
- Bump pypa/gh-action-pypi-publish from 1.8.10 to 1.8.11.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.8.10 to 1.8.11.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.8.10...v1.8.11)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #69 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.8.10. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.8.6 to 1.8.10
- Bump pypa/gh-action-pypi-publish from 1.8.6 to 1.8.10.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.8.6 to 1.8.10.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.8.6...v1.8.10)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #70 from
  DynamicTimeWarping/dependabot/github_actions/actions/checkout-4. [Toni
  G]

  Bump actions/checkout from 3 to 4
- Bump actions/checkout from 3 to 4. [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 3 to 4.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v3...v4)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #71 from
  DynamicTimeWarping/dependabot/github_actions/codecov/codecov-action-4.
  [Toni G]

  Bump codecov/codecov-action from 3 to 4
- Bump codecov/codecov-action from 3 to 4. [dependabot[bot]]

  Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 3 to 4.
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v3...v4)

  ---
  updated-dependencies:
  - dependency-name: codecov/codecov-action
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Merge pull request #73 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.16.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.13.1 to 2.16.0
- Bump pypa/cibuildwheel from 2.13.1 to 2.16.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.13.1 to 2.16.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.13.1...v2.16.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #61 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.13.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.12.3 to 2.13.1
- Bump pypa/cibuildwheel from 2.12.3 to 2.13.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.12.3 to 2.13.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.12.3...v2.13.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #58 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.8.6. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.6.4 to 1.8.6
- Bump pypa/gh-action-pypi-publish from 1.6.4 to 1.8.6.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.6.4 to 1.8.6.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.6.4...v1.8.6)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #57 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.12.3.
  [Toni G]

  Bump pypa/cibuildwheel from 2.12.0 to 2.12.3
- Bump pypa/cibuildwheel from 2.12.0 to 2.12.3. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.12.0 to 2.12.3.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.12.0...v2.12.3)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #47 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.12.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.11.3 to 2.12.0
- Bump pypa/cibuildwheel from 2.11.3 to 2.12.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.11.3 to 2.12.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.11.3...v2.12.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #45 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.6.4. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.6.1 to 1.6.4
- Bump pypa/gh-action-pypi-publish from 1.6.1 to 1.6.4.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.6.1 to 1.6.4.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.6.1...v1.6.4)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #43 from
  DynamicTimeWarping/dependabot/github_actions/pypa/gh-action-pypi-
  publish-1.6.1. [Toni G]

  Bump pypa/gh-action-pypi-publish from 1.5.1 to 1.6.1
- Bump pypa/gh-action-pypi-publish from 1.5.1 to 1.6.1.
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.5.1 to 1.6.1.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.5.1...v1.6.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Merge pull request #44 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.11.3.
  [Toni G]

  Bump pypa/cibuildwheel from 2.11.2 to 2.11.3
- Bump pypa/cibuildwheel from 2.11.2 to 2.11.3. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.11.2 to 2.11.3.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.11.2...v2.11.3)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #41 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.11.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.11.1 to 2.11.2
- Bump pypa/cibuildwheel from 2.11.1 to 2.11.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.11.1 to 2.11.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.11.1...v2.11.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #40 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.11.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.10.2 to 2.11.1
- Bump pypa/cibuildwheel from 2.10.2 to 2.11.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.10.2 to 2.11.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.10.2...v2.11.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...
- Update issue templates. [Toni G]
- Merge pull request #37 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.10.2.
  [Toni G]

  Bump pypa/cibuildwheel from 2.10.1 to 2.10.2
- Bump pypa/cibuildwheel from 2.10.1 to 2.10.2. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.10.1 to 2.10.2.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.10.1...v2.10.2)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #35 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.10.1.
  [Toni G]

  Bump pypa/cibuildwheel from 2.10.0 to 2.10.1
- Bump pypa/cibuildwheel from 2.10.0 to 2.10.1. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.10.0 to 2.10.1.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.10.0...v2.10.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Merge pull request #34 from
  DynamicTimeWarping/dependabot/github_actions/pypa/cibuildwheel-2.10.0.
  [Toni G]

  Bump pypa/cibuildwheel from 2.9.0 to 2.10.0
- Bump pypa/cibuildwheel from 2.9.0 to 2.10.0. [dependabot[bot]]

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.9.0 to 2.10.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.9.0...v2.10.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...


v1.3.0 (2022-09-02)
-------------------
- Raise error if unknown plot type. [Toni]
- Coverage. [Toni]
- Do not call plt.show() [Toni]
- Ignore backup files. [Toni]


v1.2.3 (2022-09-02)
-------------------
- Last before bumpversion. [Toni]
- Plot two way now converts xts to numpy. [Toni]
- Fix https://github.com/DynamicTimeWarping/dtw-python/issues/33. [Toni]
- Apidocs reqs. [Toni]
- Different detection whether running interactively. [Toni G]
- Delete .travis.yml. [Toni G]
- Bump pypa/cibuildwheel from 2.8.1 to 2.9.0 (#30) [Toni G,
  dependabot[bot], dependabot[bot]]

  * Bump pypa/cibuildwheel from 2.8.1 to 2.9.0

  Bumps [pypa/cibuildwheel](https://github.com/pypa/cibuildwheel) from 2.8.1 to 2.9.0.
  - [Release notes](https://github.com/pypa/cibuildwheel/releases)
  - [Changelog](https://github.com/pypa/cibuildwheel/blob/main/docs/changelog.md)
  - [Commits](https://github.com/pypa/cibuildwheel/compare/v2.8.1...v2.9.0)

  ---
  updated-dependencies:
  - dependency-name: pypa/cibuildwheel
    dependency-type: direct:production
    update-type: version-update:semver-minor
  ...


v1.2.2 (2022-07-27)
-------------------
- Bump pypa/gh-action-pypi-publish from 1.5.0 to 1.5.1 (#25)
  [dependabot[bot]]

  Bumps [pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) from 1.5.0 to 1.5.1.
  - [Release notes](https://github.com/pypa/gh-action-pypi-publish/releases)
  - [Commits](https://github.com/pypa/gh-action-pypi-publish/compare/v1.5.0...v1.5.1)

  ---
  updated-dependencies:
  - dependency-name: pypa/gh-action-pypi-publish
    dependency-type: direct:production
    update-type: version-update:semver-patch
  ...
- Bump actions/checkout from 2 to 3 (#26) [dependabot[bot]]

  Bumps [actions/checkout](https://github.com/actions/checkout) from 2 to 3.
  - [Release notes](https://github.com/actions/checkout/releases)
  - [Changelog](https://github.com/actions/checkout/blob/main/CHANGELOG.md)
  - [Commits](https://github.com/actions/checkout/compare/v2...v3)

  ---
  updated-dependencies:
  - dependency-name: actions/checkout
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Bump actions/setup-python from 2 to 4 (#27) [dependabot[bot]]

  Bumps [actions/setup-python](https://github.com/actions/setup-python) from 2 to 4.
  - [Release notes](https://github.com/actions/setup-python/releases)
  - [Commits](https://github.com/actions/setup-python/compare/v2...v4)

  ---
  updated-dependencies:
  - dependency-name: actions/setup-python
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Bump codecov/codecov-action from 2 to 3 (#28) [dependabot[bot]]

  Bumps [codecov/codecov-action](https://github.com/codecov/codecov-action) from 2 to 3.
  - [Release notes](https://github.com/codecov/codecov-action/releases)
  - [Changelog](https://github.com/codecov/codecov-action/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/codecov/codecov-action/compare/v2...v3)

  ---
  updated-dependencies:
  - dependency-name: codecov/codecov-action
    dependency-type: direct:production
    update-type: version-update:semver-major
  ...
- Create dependabot.yml. [Toni G]
- Update build_wheels.yml. [Toni G]
- Update build_wheels.yml. [Toni G]
- Update build_wheels.yml. [Toni G]


v1.2.0 (2022-07-25)
-------------------
- Changelog. [Toni]


v1.1.15 (2022-07-25)
--------------------
- Fix license. [Toni]
- Fix license files. [Toni]
- Reference time series is now plotted on the same (#23) [Nicholas
  Livingstone, Nicholas Livingstone]

  axis as the query. In the event of a non-zero offset, the reference
  values are adjusted by the offset and an offset twin axis is generated with the
  same scale of the original axis.
- Update build_wheels.yml. [Toni G]


v1.1.14 (2022-06-17)
--------------------
- Last before bumpversion. [Toni]
- Push tags. [Toni]
- Disable warparea test. [Toni]
- Disable warparea test. [Toni]
- Disable warparea test. [Toni]


v1.1.13 (2022-06-17)
--------------------
- Last before bumpversion. [Toni]
- Update warpArea.py. [Toni G]
- Cibuildwheel2 (#19) [Toni G]

  * test updated ci

  * new

  * update codecov action

  * archs

  * auto64

  * skip musl
- Added axes labels for dtwPlotTwoWay (#15) [Boje Deforce]

  Axes labels were not being added in the dtwPlotTwoWay function. This is now added.


v1.1.12 (2022-01-14)
--------------------
- Last before bumpversion. [Toni]
- Fix license. [Toni]


v1.1.11 (2022-01-14)
--------------------
- Last before bumpversion. [Toni]
- Vectorized window functions. [Toni]


v1.1.10 (2021-04-10)
--------------------
- Last before bumpversion. [Toni]
- Maint. [Toni]
- Maint. [Toni]
- Maintenance. [Toni]
- Build maintenance. [Toni]


v1.1.9 (2021-04-10)
-------------------
- Last before bumpversion. [Toni]
- Made cython necessary for building. [Toni]
- Revert misguided Makefile. [Toni]


v1.1.8 (2021-04-10)
-------------------
- Changelog. [Toni]
- Last before bumpversion. [Toni]
- Update cython. fix np.int warning. [Toni]
- Update setup.py. [Toni G]
- Raise numpy requirements. [Toni G]


v1.1.7 (2021-03-24)
-------------------
- Last before bumpversion. [Toni]
- Last before bumpversion. [Toni]
- Add universal binaries. [Toni G]
- Update cibuildwheel (#10) [Toni G]

  * Update build.yml

  * Update build.yml
- Roxygen works again, revamped docs. [Toni]
- New maint code. [Toni]
- Note on abandoning autogen. [Toni]
- Merge from R. [Toni]


v1.1.6 (2020-09-25)
-------------------
- Last before bumpversion. [Toni]
- Merged with R. [Toni]


v1.1.5 (2020-06-22)
-------------------
- Remove runtime dep on setuptools. [Toni]
- Badges. [Toni]
- Codecov. [Toni]
- Codecov. [Toni]
- Codecov. [Toni]
- Codecov. [Toni]
- Changelog. [Toni]


v1.1.4 (2020-06-19)
-------------------
- Add callable main. cleanups. [Toni]


v1.1.3 (2020-06-18)
-------------------
- Doctests again. [Toni]


v1.1.2 (2020-06-18)
-------------------
- Ci doctests. [Toni]


v1.1.1 (2020-06-18)
-------------------
- Doctests. [Toni]
- Improve warp and docs. [Toni]


v1.1.0 (2020-06-18)
-------------------
- Before bump. [Toni]
- Dont cythonize in build. [Toni]
- Test deployer. [Toni]
- Python version. [Toni]
- Absolute imports. [Toni]

  abs imports
- Test setup requires. [Toni]
- Test cibuildwheel. [Toni]
- Added test for issue https://github.com/DynamicTimeWarping/dtw-
  python/issues/5. [Toni]


v1.0.6 (2020-06-17)
-------------------
- Fixed subtle bug with open_begin. [Toni]
- Adding CRAN test equivalent. [Toni]
- Fixes https://github.com/DynamicTimeWarping/dtw-python/issues/5.
  [Toni]


v1.0.5 (2020-02-24)
-------------------
- Fix for open-end with slope-constrained alignments. [Toni]
- Merge pull request #3 from tcwalther/fix-slantedbandwindow. [Toni G]

  fix slantedBandWindow function - thanks!
- Fix slantedBandWindow function. [Thomas Walther]

  The previous version had variable names such as query.size in it
   - notation which is common in R, but doesn't work in Python.
   This commit corrects these names to query_size, reference_size
   and window_size, respectively.


v1.0.4 (2019-12-30)
-------------------
- Fixes https://github.com/DynamicTimeWarping/dtw-python/issues/1.
  [Toni]


v1.0.3 (2019-10-31)
-------------------
- Possible fix for windows. [Toni]
- Conda env. [Toni]


v1.0.2 (2019-09-04)
-------------------
- Minor fixes. [Toni]
- Aami doctests maybe. [Toni]


v1.0.1 (2019-09-01)
-------------------
- Last before bumpversion. [Toni]
- Misc bugs. [Toni]


v0.5.2 (2019-08-31)
-------------------
- Last before bumpversion. [Toni]


v0.5.1 (2019-08-31)
-------------------
- Last before bumpversion. [Toni]


v0.5.0 (2019-08-31)
-------------------
- Docs index. [Toni]
- Fixup docs. [Toni]
- Automodapi. [Toni]
- Using bootstrap theme. [Toni]


v0.4.0 (2019-08-30)
-------------------
- Renames. [Toni]
- Rename. [Toni]


v0.3.10 (2019-08-30)
--------------------
- Make release. [Toni]


v0.3.9 (2019-08-30)
-------------------
- Make release. [Toni]


v0.3.7 (2019-08-30)
-------------------
- Setup. [Toni]


v0.3.6 (2019-08-30)
-------------------
- Return axes plot. [Toni]


v0.3.0 (2019-08-29)
-------------------
- C file. [Toni]


v0.2.0 (2019-08-29)
-------------------
- Doctests. [Toni]
- Dtw doc. [Toni]
- Squash spaces. [Toni]
- Tests. [Toni]
- Rename. [Toni]
- Progress. [Toni]
- Going for tests. [Toni]
- Checkpoint. [Toni]
- Testing examples. [Toni]
- New docs. [Toni]
- Hide _get_p. [Toni]
- Entry point. [Toni]
- Remove dependency on click. [Toni]
- Tests. [Toni]
- Test cli. [Toni]
- Cli ok. [Toni]
- Attempt at reformat. [Toni]


v0.1.1 (2019-08-27)
-------------------
- Underscore. [Toni]
- Density. [Toni]
- W2 works. [Toni]
- Lambda error. [Toni]
- Plot2. [Toni]
- Plots. [Toni]
- Step pattern by name. [Toni]
- Renamed internal modules. [Toni]
- Renaming. [Toni]
- Renaming. [Toni]
- Renaming package. [Toni]
- Markdown conversion. [Toni]
- Progress. [Toni]
- Docs in. [Toni]
- Added tags. [Toni]
- Inserting ok. [Toni]
- Checkpoint. [Toni]
- Abort. [Toni]
- Abort roxypick. [Toni]
- Headers. [Toni]
- Plot step pattern. [Toni]
- Countpaths. [Toni]
- Countpaths. [Toni]
- Mkdirdeltas. [Toni]
- Windowing. [Toni]
- Mvm, bt. [Toni]
- Object. [Toni]
- Progress. [Toni]
- All patterns ok. [Toni]
- Checkpoint. [Toni]
- Pattern building. [Toni]
- Listed step patterns. [Toni]
- Print and T. [Toni]
- Test ok. [Toni]
- Builds. [Toni]
- Checkpoint. [Toni]
- More import. [Toni]
- Initial import. [Toni]
- Initial commit. [Toni G]


