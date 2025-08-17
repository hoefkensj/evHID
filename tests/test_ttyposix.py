# /usr/bin/env pyhthon
from evHID.Types.tty.posix import KBTty



with KBTty() as kb:
	while True:
		if kb.event:
			key=kb.getch()
			print(key)
			if key=='q':
				break
