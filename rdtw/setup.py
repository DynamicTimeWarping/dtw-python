from __future__ import division, print_function, absolute_import


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration

    config = Configuration('rdtw', parent_package, top_path)

    config.add_extension('_dtw_utils',
                         sources=['dtw_computeCM.c','_dtw_utils.c'])

    return config


if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
