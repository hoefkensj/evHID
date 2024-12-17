#!/usr/bin/env python
from signal import signal, SIGUSR1
from time import sleep

from Clict import Clict
from pynput import keyboard

from evHID.Types.data import fullkey
from evHID.Types.dev.keyboard import KBDev
from evHID.Types.term.posix import Term
from evHID.Types.tty import KBTty


class KBEV_Posix(Clict):
	def __init__(__s,*a,**k):
		super().__init__()
		__s.term = k.get('term',Term())
		__s.callback={}
		__s.callback['kd']=k.get('kd', lambda key : None)
		__s.callback['ku']=k.get('ku', lambda key : None)
		__s.mode=__s.__mode__
		__s._dev = KBDev
		__s._tty = KBTty
		__s._key=None
		__s._keys=[None,]
		__s._event=False
		__s.dev=__s._dev(parent=__s)
		__s.tty=__s._tty(__s)
		__s.handlers=__s.__sigrecv__()
		__s.__create__()
	
	def clearstdin(__s,key):
		K=keyboard.Key
		if key in [K.space, K.enter, K.home, K.end, K.page_down, K.page_up,K.tab]:
			stdin = __s.tty.read(1)
		elif key in [K.shift,K.shift_l,K.shift_r,K.caps_lock,K.ctrl,K.alt,K.alt_gr,K.num_lock,K.scroll_lock,K.pause,K.print_screen]:
			stdin=__s.tty.read(0)
		elif 'value' in dir(key):
			stdin = __s.tty.read(3)
		elif 'char' in dir(key):
			stdin = __s.tty.read(1)
		
	def __sigrecv__(__s):

		def receive_dev(signum, stack):
			if __s.tty.event:
				key=__s.dev.key()
				__s.clearstdin(key)
				__s._key=key
				__s._event=True
		__s.s1=signal(SIGUSR1, receive_dev)

	def event(__s):
		ev=__s._event
		__s._event=False
		return ev
	
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

	# 	return
	# 	__s
	def __exit__(__s,*a,**k):
		__s.dev.__exit__()


	def __mode__(__s,n):
		__s.term.mode('ctl')

	def key(__s):
		K=keyboard.Key
		key=__s._key
		fk= fullkey(key)
		if key == K.space:
			fk.name='space'
			fk.val=20
			fk.chr=' '
			fk.key=key
		else:
			if 'name' in dir(key):
				fk.name=str(key.name).split('.')[-1]
			else:
				fk.name=repr(key)
			
			if 'char' in dir(key):
				fk.chr=key.char
			else:
				fk.chr=None
			
			if 'value' in dir(key):
				fk.val=int(str(key.value)[1:-1])
			else:
				if 'char' in dir(key):
					if key.char is not None:
						fk.val=ord(key.char)
			__s._key=None
		return fk

	def getCode(__s):
		code=None
		if __s.dev._event:
			key=__s.__getKBKey__()
			code=key
			# sys.stdin.read(key.clr)
			
			if 'value' in dir(key):
				if key == keyboard.Key.space:
					code=ord(str(key.value)[1:-1])
				else:
					code=int(str(key.value)[1:-1])
			elif 'char' in dir(key):
				code = ord(key.char)
			else:
				print(f'\x1b[8;1H\x1b[K{key}')
				print(f'\x1b[9;1H\x1b[K{dir(key)}')

		return code
	def __getKBKey__(__s):
		def getstdin(key):
			K=keyboard.Key
			stdin=''
			if key in [K.space,K.enter,K.home,K.end,K.page_down,K.page_up]:
					stdin=__s.tty.read(1)
			elif 'value' in dir(key):
				stdin=__s.tty.read(3)
			elif 'char' in dir(key):
				stdin = __s.tty.read(1)
			return stdin
		
		def getkbkey():
			key=__s.dev.getkey()
			keys=[key,getstdin(key)]
			
			return keys
		keyc=None
		while not keyc:
			if __s.dev._len>0:
				keyc=getkbkey()
				break
			sleep(1e-6)
		return keyc

# __s.callback
# k.get('key'k.get('chr')k.get('val')
