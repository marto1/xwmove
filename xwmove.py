#!/usr/bin/python
import argparse
from ewmh import EWMH
from posinfo import MainInfo
from move import WindowMove
from config import DEBUG
import sys

def runner():
    parser = argparse.ArgumentParser(description='Move windows around.')
    parser.add_argument('-d','--double-command', action="store_true",
                        dest='double',
                        help='If this is set the double command mode will activate',
                        )
    if sys.argv[1:]:
        parser.add_argument('direction', type=str,
                        help='direction that you want to move',
                        choices=('bottomright', 'bottomleft', 'topleft', 'topright',
                        'center', 'top', 'right', 'bottom', 'left',), nargs=1,
                        )
    else:
        parser.add_argument('--direction', default = ['center'])
    args = parser.parse_args()

    ewmh = EWMH()
    main = MainInfo(ewmh)
    moveWin = WindowMove(main)

    if (DEBUG):
        import pprint
        print 'DOUBLE MODE:',args.double
        pprint.pprint(vars(main))
    moveWin.move(ewmh.getActiveWindow(), args.direction[0], 'half')

    return 0

if __name__ == '__main__':
    sys.exit(runner())