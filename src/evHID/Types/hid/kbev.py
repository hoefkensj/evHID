#!/usr/bin/env python
from signal import signal, SIGUSR1
from time import sleep
import sys
from Clict import Clict
from pynput import keyboard
import time
from evHID.Types.data import FullKey
from evHID.Types.dev.keyboard import KBDev
from evHID.Types.term.posix import Term
from evHID.Types.tty import KBTty

class KBEV_Posix(Clict):
	def __init__(__s,*a,**k):
		super().__init__()
		__s.term = k.get('term',Term())
		__s.cbs=k.get('cb',{})
		__s.mode=__s.__mode__
		__s._dev = KBDev
		__s._tty = KBTty
		__s._key=None
		__s._keys=[None,]
		__s._history=[None,]
		__s._chars=[]
		__s._event=False
		__s._focus=True
		__s.noevkeys=['shift', 'alt', 'ctrl', 'caps_lock', 'cmd', 'num_lock', 'shift_r', 'ctrl_r', 'alt_r','cmd_r']
		__s.callbacks=k.get('cb',[])
		__s.cb={'glob':{'kd':[],'ku':[]}}
		__s.dev=__s._dev(parent=__s)
		__s.tty=__s._tty(__s)
		__s.handlers=__s.__sigrecv__()
		for cb in __s.callbacks:
			__s.addcallback(cb)
		__s.__create__()


	def __sigrecv__(__s):
		def receive_dev(signum, stack):
			key=__s._key
			focusev=__s.tty.event
			if not focusev:
				__s._focus= __s._focus if key.name  in __s.noevkeys else False
			else :
				__s._focus=True
			if __s._focus:
				__s._chars=__s.tty.read()
				__s._event=True

		__s.s1=signal(SIGUSR1, receive_dev)

	def __create__(__s):
		__s.mode(1)
		__s.dev=__s._dev(parent=__s)
		__s.start=__s.dev.start
		__s.join=__s.dev.join
		__s.stop=__s.dev.stop
	
	def __enter__(__s):
		__s.__create__()
		__s.dev.__enter__()
		Key=keyboard.Key
		keyboard.Controller().tap(Key.home)
		return __s
		
	def __exit__(__s,*a,**k):
		__s.dev.__exit__()

	def __mode__(__s,n):
		__s.term.mode('ctl')

	def key(__s):
		key=__s._key
		__s._key=None
		return key

	# if key == K.space:
	def event(__s):
		ev=__s._event
		__s._event=False
		return ev

	def addcallback(s,cb):
		if cb.scope=='global':
			if 'kd' in cb.event:
				s.cb['glob']['kd']+=[cb]
			if 'ku' in cb.event:
				s.cb['glob']['ku']+=[cb]



