
import numpy
from .stepPattern import *

def mvmStepPattern(elasticity=20):
    size = elasticity

    pn = numpy.repeat( numpy.arange(size)+1, 2)
    dx = numpy.tile( [1,0], size)
    dy = pn * dx
    w = numpy.tile( [-1,1], size)

    tmp = numpy.vstack([pn, dx, dy, w]).T

    return StepPattern(tmp,"N")

