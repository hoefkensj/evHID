from pynput import keyboard
from signal import pause
from Xlib import XK
from pynput.keyboard._base import KeyCode
from Xlib.XK import string_to_keysym
from Xlib.XK import string_to_keysym,keysym_to_string,load_keysym_group,_load_keysyms_into_XK
from evHID.Types.controls.kb_key import make_Key
print()
def kd(key):
	# KeyCode.from_char()
	print(key.name,key.value)
	k=make_Key(key)

	print(k.name,k.value,k.char,k.key)


with keyboard.Listener(on_press=kd):
	pause()