Changelog
=========


(unreleased)
------------
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


