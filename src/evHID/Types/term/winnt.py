import msvcrt
msvcrt.getch().decode('utf-8')


#arrow
msvcrt.getch()  # skip 0xE0
c = msvcrt.getch()
vals = [72, 77, 80, 75]
return vals.index(ord(c.decode('utf-8')))

return msvcrt.kbhit()