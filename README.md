evHID

events in python for HID devices (currently only keyboard) that can detect everykey in the terminal:
    due to the nature of the terminal 
        - while every key is detected not every key is reported to the terminal 
            this means that when the terminal loses focus detection continues untill detectable key is pressed
        - you can pass callback functions to work globally (so key detection works in the backround aswell)
        - can be blocking or none blocking,
        -match on keys by name or value or character
            ex: if key == 'right' will match the right arrowkey
                   key == '0x20' will match the space key
        - events reported using signal:
            instead of using time.sleep(0.01) you can use 
                from signals import pause
                while True:
                    #code for matching here
                    pause()


note for self XKKEYSYMS
modifiers :
     & | 0x00ff | 00255 
     & | 0xff00 | 65280

\x1b\x5b\x41 ansiesc
             | ANSI|ASCII     | XLIB    | PYNPUT

uparrow      | 0x1b5b41  :    | 0x08FC : 2300 | 0xff52 : 65362
backspace    | \b | 0x08 :          0xFF08 : 65288| 0xfecc : 65288
-----|---------|---------|--------------------
\    | 0x5c  |         | 0x005c |   92  
esc  | 0x1b  | 0xFF1b  | 0xff1b | 65307
[    | 0x5b  | 0x005b  |        |   91
A    | 0x41  | 0x0041  |        |   65
Xlib


       |   XLIB |
keysym | 0x08FC | 2300      |up arrow
       | 0x0800 | 2048
       | 0x00FC | 0252
-------|--------|[]

=======|========|=
pynput | 0xff52 | 65362     |up arrow
       | 0x0052 |    82     | R

0x00ff0d| 65293   
        0x00ff00| 65280
        0x00000d|    13
       