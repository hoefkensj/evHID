#!/usr/bin/env python
from time import time_ns
from shutil import get_terminal_size

from evHID.Types.data import xy


class Size():
	def __init__(__s,**k):
		__s.parent=None
		__s.getsize=get_terminal_size
		__s.time=None
		__s.last=None
		__s.xy= xy(1, 1)
		__s._tmp= xy(1, 1)
		__s.rows=1
		__s.cols=1
		__s.history=[]
		__s.changed=False
		__s.changing=False
		__s.__kwargs__(**k)
		__s.init=__s.__update__()
		
	@property
	def rc(__s):
			__s.__update__()
			return (__s.cols,__s.rows)
	
	def __kwargs__(__s,**k):
		__s.term= k.get('parent')
	
	def __update__(__s):
		if __s.time is None:
			__s.last= time_ns()
		size= xy(*__s.getsize())
		if size != __s.xy:
			if size != __s._tmp:
				__s.changing = True
				__s._tmp=size
				__s._tmptime=time_ns()
			if size == __s._tmp:
				if (time_ns()-__s._tmptime) * 1e6 > 500:
					__s.changing=False
					__s.changed=True
					__s.history+=[__s.xy]
					__s.xy=size
					__s.rows = __s.xy.y
					__s.cols = __s.xy.x
				else:
					__s._tmp=size
		if size == __s.xy:
			__s.changed=False
			
#
#
#
# def __size__(__s):
# 	def readTermSize(__s, dim='xy'):
# 		if __s.size.check == 0:
# 			__s.size.check = time_ns()
# 		current = {
# 			'x': (xy := tuple([*shutil.get_terminal_size()]))[0],
# 			'y': xy[1],
# 			'xy': xy
# 			}
# 		if current != __s.size.current:
# 			__s.size.lastcheck = __s.size.check
# 			__s.size.check = time_ns()
# 			__s.size.changing = ((__s.size.check - __s.size.lastcheck) * 1e6 < 500)
# 			if not __s.size.changing:
# 				__s.size.history += [__s.size.curent]
# 				__s.size.current = current
# 				__s.size.rows = current['y']
# 				__s.size.cols = current['x']
# 				__s.size.xy = current['xy']
# 				__s.size.changed = True
# 		else:
# 			__s.size.changed = False
# 		return current[dim]
#
# 	return readTermSize(__s)
