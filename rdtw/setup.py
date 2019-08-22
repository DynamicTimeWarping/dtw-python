from __future__ import division, print_function, absolute_import

from setuptools.extension import Extension
from Cython.Build import cythonize
from numpy.distutils.misc_util import Configuration


def configuration(parent_package='', top_path=None):
    config = Configuration('rdtw', parent_package, top_path)

    config.add_extension('_dtw_utils',
                         sources=['dtw_computeCM.c','_dtw_utils.pyx'])


    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup_args=configuration(top_path='').todict()
    setup_args['ext_modules']=cythonize(setup_args['ext_modules'])
    
    setup(**setup_args)
