#!/usr/bin/env python
import sys
import termios
import tty

import evHID.Types.data


# # Open the new pseudoterminal for reading
# new_stdin_fd = os.open(new_pts, os.O_RDONLY)
#
# # Duplicate the new pseudoterminal's file descriptor onto sys.stdin
# os.dup2(new_stdin_fd, sys.stdin.fileno())
# #
def ansi(term,ansi, parser):
	tty.setcbreak(term.fd, termios.TCSANOW)
	try:
		sys.stdout.write(ansi)
		sys.stdout.flush()
		result = parser()
	finally:
		termios.tcsetattr(term.fd, termios.TCSAFLUSH, term.live)
	return result
#

# def info():
#
# 	def pos_cursor():
# 		def Parser():
# 				buf=''
# 				while buf[-1] != "R":
# 					buf += sys.stdin.read(1)
# 				# reading the actual values, but what if a keystroke appears while reading
# 				# from stdin? As dirty work around, if this fails returns None
# 				try:
# 					groups=rexy.search(buf).groupdict()
# 					result={'X': groups['X'],'Y':groups['Y']}
# 				except AttributeError:
# 					result = None
# 				return result
# 		rexy = re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R", re.VERBOSE)
# 		ansiesc='\x1b[6n'
# 		result=None
# 		while not result:
# 			result=ansi(ansiesc,Parser)
# 		return result
#
# 	def bg_color():
# 		def Parser():
# 			buf = ''
# 			for i in range(23):
# 				buf += sys.stdin.read(1)
# 			rgb=buf.split(':')[1].split('/')
# 			rgb={c:int(i,base=16) for c,i in zip([*'RGB'],rgb)}
# 			tot=[*rgb.values()]
# 			tot=sum(tot)
# 			rgb['avg']=(tot/3)/65535
# 			rgb['max']=65535
# 			return rgb
# 		ansiesc='\x1b]11;?\a'
# 		return ansi(ansiesc,Parser)
#
# 	def size():
# 		s= {'C'  :(shutil.get_terminal_size()[0]),
# 		 'L' : (shutil.get_terminal_size()[1])}
# 		return s
#
# 	term={'stdout':'not a tty'}
# 	if sys.stdout.isatty():
# 		term=Clict()
# 		term.size={**size()}
# 		term.cursor={**pos_cursor()}
# 		term.color.bg={**bg_color()}
# 		term.get_size=size
# 		term.get_cursor=pos_cursor
# 		term.get_color.bg=bg_color
# 	return term	def __cursor_hide__(__s):
# 		print('\x1b[?25l',end='',flush=True)
# 		atexit.register(__s.cursor.show)
# 	def __cursor_show__(__s):
# 		print('\x1b[?25h',end='',flush=True)
# 	def __cursor_pos_get__(__s):
# 		def Parser():
# 			buf=' '
# 			while buf[-1] != "R":
# 				buf += sys.stdin.read(1)
# 			# reading the actual values, but what if a keystroke appears while reading
# 			# from stdin? As dirty work around, getpos() returns if this fails: None
# 			try:
# 				groups=rexy.search(buf).groupdict()
# 				result={'X': groups['X'],'Y':groups['Y']}
# 			except AttributeError:
# 				result=None
# 			return result
# 		rexy= re.compile(r"^.?\x1b\[(?P<Y>\d*);(?P<X>\d*)R",re.VERBOSE)
# 		ansiesc='\x1b[6n'
# 		result=None
# 		while not result:
# 			result=ansi(ansiesc,Parser)
# 		return result


if __name__ == '__main__' :

		T = Term()
		print(T.cursor.x())
		print(T.cursor.Y)
		print(T.cursor.X)
		print(T.cursor.y())
		print(evHID.Types.data.color.bg.rgb())
