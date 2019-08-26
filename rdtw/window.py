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


#IMPORT_RDOCSTRING noWindow
#ENDIMPORT


def noWindow(iw, jw, query_size, reference_size):
    return True

def sakoeChibaWindow(iw, jw, query_size, reference_size, window_size):
    ok = abs(jw-iw) <= window_size
    return ok

def itakuraWindow(iw, jw, query_size, reference_size):
	n<-query_size
	m<-reference_size
	ok =	(jw <  2*iw) and \
		(iw <= 2*jw) and \
		(iw >= n-1-2*(m-jw)) and \
		(jw >  m-1-2*(n-iw))
	return ok

   

def slantedBandWindow(iw, jw, query_size, reference_size, window_size):
    diagj = (iw*reference.size/query.size)
    return abs(jw-diagj)<=window.size;




