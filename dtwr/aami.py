##
## Copyright (c) 2006-2019 of Toni Giorgino
##
## This file is part of the DTW package.
##
## DTW is free software: you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## DTW is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.
##
## You should have received a copy of the GNU General Public License
## along with DTW.  If not, see <http://www.gnu.org/licenses/>.
##



#IMPORT_RDOCSTRING aami
"""ANSI/AAMI EC13 Test Waveforms, 3a and 3b


ANSI/AAMI EC13 Test Waveforms 3a and 3b, as obtained from the PhysioBank
database.


**Details**

The following text is reproduced (abridged) from PhysioBank, page
https://www_physionet_org/content/aami-ec13/1_0_0/. Other recordings
belong to the dataset and can be obtained from the same page.

The files in this set can be used for testing a variety of devices that
monitor the electrocardiogram. The recordings include both synthetic and
real waveforms. For details on these test waveforms and how to use them,
please refer to section 5_1_2_1, paragraphs (e) and (g) in the reference
below. Each recording contains one ECG signal sampled at 720 Hz with
12-bit resolution.



Parameters
----------




Returns
-------

(None)


Notes
-----

Timestamps in the datasets have been re-created at the indicated
frequency of 720 Hz, whereas the original timestamps in ms (at least in
text format) only had three decimal digits’ precision, and were
therefore affected by substantial jittering.





"""
#ENDIMPORT

import numpy
from pkg_resources import resource_string



aami3a = numpy.fromstring( resource_string(__name__, '../data/aami3a.csv') , sep="\n" )
aami3b = numpy.fromstring( resource_string(__name__, '../data/aami3b.csv') , sep="\n" )
