#!/usr/bin/env python
import sys

from evHID.Types.data import color


class Colors():
	def __init__(__s,**k):
		__s.parent=None
		__s.specs={'fg': 10 , 'bg': 11}
		__s._ansi='\x1b]{spec};?\a'
		__s.__kwargs__(**k)
		__s.fg= color(255, 255, 255)
		__s.bg= color(0, 0, 0)
		__s.init=__s.__update__()

	def __kwargs__(__s,**k):
		__s.term= k.get('parent')

	@staticmethod
	def _ansiparser_():
		buf = ''
		try:
			for i in range(23):
				buf += sys.stdin.read(1)
			rgb=buf.split(':')[1].split('/')
			rgb=[int(i,base=16)for i in rgb]
			rgb= color(*rgb, 16)
		except Exception as E:
			print(E)
			rgb=None
		return rgb
	
	def __update__(__s):
		for ground in __s.specs:
			result=None
			while not result:
				result = __s.term.ansi( __s._ansi.format(spec=__s.specs[ground]), __s._ansiparser_)
			__s.__setattr__(ground,result)

		return {'fg':__s.fg,'bg':__s.bg}
