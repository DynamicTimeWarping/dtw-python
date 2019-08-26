

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




