

import numpy
from pkg_resources import resource_string


aami3a = numpy.fromstring( resource_string(__name__, '../data/aami3a.csv') , sep="\n" )
aami3b = numpy.fromstring( resource_string(__name__, '../data/aami3b.csv') , sep="\n" )
