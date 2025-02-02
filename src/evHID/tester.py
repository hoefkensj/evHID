# from hashlib import file_digest
# from operator import truediv
# from os import eventfd
# from select import select
# from evHID.Types.term.posix import Term
# import sys
# from time import sleep
#
# term=Term()
# term.mode('ctl')
# fd=sys.stdin.fileno()
# event=False
# while True:
# 	a,b,c=select([fd], [], [], 0)
# 	if a!=[]:
# 		event=True
# 	if event:
# 		while a!=[]:
# 			a, b, c = select([fd], [], [], 0)
# 			print('\x1b[5;5H\x1b[31mEvent\x1b[m')
# 			cc=sys.stdin.read(1)
# 			print(f'\x1b[6;5H\x1b[31m{cc}\x1b[m')
# 		event=False
#
# 	else:
# 		print('\x1b[5;5H\x1b[32mevent\x1b[m')
# 	sleep(0.05)

import sys
from select import select
from time import sleep
from evHID.Types.term.posix import Term

term = Term()
term.mode('ctl')
fd = sys.stdin.fileno()
buffer=[]
while True:
	event= select([fd], [], [], 0)[0]

	if event:
		print('\x1b[5;5H\x1b[31mEvent\x1b[m')
		while event:
			buffer+=[c:= sys.stdin.read(1)]
			print(f'\x1b[6;5H\x1b[31m{c}\x1b[m')
			print(f'\x1b[7;5H\x1b[32m{"".join(buffer)}\x1b[m')
			event = select([fd], [], [], 0)[0]
	else:
		print('\x1b[5;5H\x1b[32mevent\x1b[m')
	sleep(0.1)


