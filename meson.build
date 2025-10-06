project('dtw-python', ['c', 'cython'], version: '1.5.3', license: 'GPL-2.0-or-later', default_options: ['warning_level=1'])

py = import('python').find_installation(modules: ['cython', 'numpy'])

py.install_sources(
  'dtw/__init__.py',
  'dtw/__main__.py',
  'dtw/_backtrack.py',
  'dtw/_globalCostMatrix.py',
  'dtw/_dtw_utils_py.py',
  'dtw/countPaths.py',
  'dtw/dtw.py',
  'dtw/dtwPlot.py',
  'dtw/dtw_test_data.py',
  'dtw/mvm.py',
  'dtw/stepPattern.py',
  'dtw/warp.py',
  'dtw/warpArea.py',
  'dtw/window.py',
  subdir: 'dtw',
  pure: true,
)

py.install_sources(
  'dtw/data/README.txt',
  'dtw/data/aami3a.csv',
  'dtw/data/aami3b.csv',
  subdir: 'dtw/data',
  pure: true,
)

dtw_include = include_directories('dtw')

numpy_inc_result = run_command(py, ['-c', 'import numpy; print(numpy.get_include())'], check: true)
numpy_include_dir = numpy_inc_result.stdout().strip()
numpy_c_args = ['-I' + numpy_include_dir]

py.extension_module(
  'dtw._dtw_utils',
  [
    'dtw/_dtw_utils.pyx',
    'dtw/dtw_core.c',
  ],
  include_directories: [dtw_include],
  c_args: numpy_c_args,
  install: true,
)
