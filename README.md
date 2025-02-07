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


