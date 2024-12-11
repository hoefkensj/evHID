#!/usr/bin/env python
import os
from signal import SIGUSR1

from pynput import keyboard



class KBDev():
	def __init__(__s,**k):
		__s.__kwargs__(**k)
		__s.sig=SIGUSR1
		__s._listener=keyboard.Listener
		__s._key=None
		__s._keys_down=[None,]
		__s._keys_hist=[None,]
		__s.__create__()

	def __kwargs__(__s,**k):
		__s.term=k.get('term')
		__s.parent=k.get('parent')
		__s.callback = {
			'kd' : k.get('kd',lambda*a,**k:None),
			'ku' : k.get('ku',lambda*a,**k:None),}
	
	
	
		if __s.parent is not None:
			__s.callback= __s.parent.callback
			__s.term=__s.parent.term
	
	def __keydown__(__s,key):
		__s.__local_kd__(key)
		__s.callback['kd'](key)
		__s.__signal__()

		
	def __keyup__(__s,key):
		__s.__local_ku__(key)
		__s.callback['ku'](key)
	
	def setkd(__s,fn):
		__s.callback_kd=fn
		__s.__create__()
	def setku(__s,fn):
		__s.callback_ku=fn
		__s.__create__()

		
	
	def __create__(__s):

		cb={'on_press':__s.__keydown__,
		'on_release':__s.__keyup__
		}
		__s.listener = __s._listener(**cb)
		__s.start=__s.listener.start
		__s.join=__s.listener.join
		__s.stop=__s.listener.stop
		return __s

	def __enter__(__s):
		__s.__create__()
		__s.start()
		return __s


	def __exit__(__s,*a,**k):
		__s.stop()

	def __local_kd__(__s,key):
		__s._key=key
		__s._keys_down=[*set([*__s._keys_down,key])]

	def __local_ku__(__s,key):
		__s._keys_down=[*set([*__s._keys_down,key])]
		__s._keys_down.remove(key)
		__s._keys_hist+=[key]





	def __signal__(__s):
		os.kill(__s.term.pid, __s.sig)
		
	def key(__s):
		key=__s._key
		__s._key=None
		return key
