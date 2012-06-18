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

moveWin = WindowMove(main)

for pos in ['bottomright', 'bottomleft', 'topleft', 'topright', 'center',
            'top', 'right', 'bottom', 'left', 'top']:
    moveWin.move(ewmh.getActiveWindow(), pos, 'half')
    time.sleep(0.5)