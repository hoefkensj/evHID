#!/usr/bin/env python
from evHID.Types.hid.kbev import KBEV_Posix
from pynput import keyboard
### how this shit should work ideallly
# keypress-> triggers event trought device listener
# -> checks for readable on stdin if so the key was meant for us
# -> reads key from the device buffer
# -> uses that to clear number of chars from stdin
# -> key gets added to global buffer
# -> getkey pops last key from buffer
# -> getkeys gets all from buffer and wipes buffer


from time import sleep

if __name__ == '__main__':
	pynspace=keyboard.Key.space

	with KBEV_Posix() as kb:
		while True:
			if kb.event():
				key=kb.key()
			sleep(0.05)

		#
		# def handle_signal(signum, frame):
		# 	print(f"Custom signal {signum} received, handling the signal.")
		# 	exit(0)
		#
		#
		# # Set the signal handler for SIGUSR1
		# signal.signal(signal.SIGUSR1, handle_signal)

			# print('..',end='',flush=True)
			# sleep(0.5)
			# print('..',end='',flush=True)
			# sleep(0.5)
			# print('..',end='',flush=True)
