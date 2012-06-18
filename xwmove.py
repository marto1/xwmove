#!/usr/bin/python
import argparse
from ewmh import EWMH
from posinfo import MainInfo
from move import WindowMove
from config import DEBUG
import sys

def runner():
    parser = argparse.ArgumentParser(description='Move windows around.')
    parser.add_argument('direction', type=str,
                    help='direction that you want to move',
                    choices=('bottomright', 'bottomleft', 'topleft', 'topright',
                    'center', 'top', 'right', 'bottom', 'left',), nargs=1)

    args = parser.parse_args()

    ewmh = EWMH()
    main = MainInfo(ewmh)
    moveWin = WindowMove(main)

    if (DEBUG):
        print 'ACTIVE WIN:',ewmh.getActiveWindow()
        print 'DIRECTION:',args.direction[0]
        print 'MAIN W:',main.mainW,'MAIN H:',main.mainH
        print 'FULL W:',main.FULL_W,'FULL H',main.FULL_H
    moveWin.move(ewmh.getActiveWindow(), args.direction[0], 'half')

    return 0

if __name__ == '__main__':
    sys.exit(runner())