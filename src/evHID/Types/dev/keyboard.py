#!/usr/bin/env python
import os
import time
from signal import SIGUSR1
from pynput import keyboard
from evHID.Types.term.posix import Term
from evHID.Types.data import FullKey


class KBDev():
	def __init__(s,**k):
		s.sig=SIGUSR1
		s.listen=keyboard.Listener
		s.parent=None
		s.term=None
		s.cb={'kd':[],'ku':[]}
		s.history=[]
		s.__kwargs__(**k)


		s._key=None
		s._keys_down=[None,]
		s._keys_hist=[None,]
		s.__create__()


	def __kwargs__(s,**k):
		p=k.get('parent')
		t=k.get('term',Term())
		s.term=t
		if p is not None:
			s.parent=p
			s.term=p.term
			for cb in p.cb['glob']['kd']:
				s.cb['kd']+=[cb]
			for cb in p.cb['glob']['ku']:
				s.cb['ku']+=[cb]


	def __keydown__(s,key):
		fkey=FullKey(key)
		s.key=fkey
		ev={'event': 'dn','key':fkey}
		for cb in s.cb['kd']:
			cb(ev)
		s.signal__()
		s.__buildin_kd__()


	def __keyup__(s,key):
		fkey=FullKey(key)
		s.__buildin_ku__(fkey)



	def __create__(s):

		cb={'on_press':s.__keydown__,
			'on_release':s.__keyup__
			}
		s.listener = s.listen(**cb)
		s.start=s.listener.start
		s.join=s.listener.join
		s.stop=s.listener.stop
		return s

	def __enter__(s):
		s.__create__()
		s.start()
		return s


	def __exit__(s,*a,**k):
		s.stop()

	def __buildin_kd__(s):
		s._keys_down=[*set([*s._keys_down,s.key])]

	def __buildin_ku__(s,key):
		s._keys_down=[*set([*s._keys_down,key])]
		s._keys_down.remove(key)
		s._keys_hist+=[key]


	def signal__(s):
		os.kill(s.term.pid, s.sig)

	def addcallback(s,cb):
		if cb.event == 'kd':
			s.cb['kd']+=[cb]
		if cb.event == 'ku':
			s.cb['ku']+=[cb]
	@property
	def key(s):
		key=s._key
		s._key=None
		return key

	@key.setter
	def key(s,key):
		s._key=key
		s.parent._key=key
