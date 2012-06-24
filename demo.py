#!/usr/bin/python
from posinfo import *
from move import *
import time

ewmh = EWMH()
main = MainInfo(ewmh)

print main.mainW
print main.mainH
print main.HALF_W, main.HALF_H
print ewmh.NET_WM_STATES
print ewmh.NET_WM_ACTIONS

moveWin = DispatchMove(main, True)

for pos in ['bottomright', 'bottomleft', 'topleft', 'topright', 'center',
            'center','top', 'right', 'bottom', 'left', 'top',]:
    moveWin.move(ewmh.getActiveWindow(), pos)
    time.sleep(0.5)