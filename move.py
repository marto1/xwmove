from ewmh import EWMH
import posinfo


class WindowMove:
    """
    Dispatches window moving.
    """

    def __init__(self, info):

        self.info = info

        self.win = None
        self.x = 0
        self.y = 0
        self.w = 1
        self.h = 1

    def move(self, window, where = 'center', size = 'full'):
        """
        Resolve the right coordinates and move the window.
        window -- win object
        where -- string literal describing the wanted positionig
        size -- sting literal describing the wanted size.
        """
        self.win = window

        if (where in ['center']):
            self.x = self.info.QUARTER_W
            self.y = self.info.QUARTER_H

        if (where in ['topleft', 'bottomleft', 'top', 'left', 'bottom']):
            self.x = self.info.topX

        if (where in ['topright', 'bottomright', 'right']):
            self.x = self.info.topRightHalfX

        if (where in ['topleft','topright', 'top', 'left',
                'right']):
            self.y = self.info.topY

        if (where in ['bottomleft','bottomright', 'bottom']):
            self.y = self.info.bottomLeftY

        if (size == 'half'):
            self.w, self.h = self.info.HALF_W, self.info.HALF_H

        if (where in ['top', 'bottom']):
            self.w = self.info.FULL_W
        if (where in ['left', 'right']):
            self.h = self.info.FULL_H

        self._move()

    def _move(self):
        """
        Move the window to the given coordinates and flush.
        """
        self.info.ewmh.setWmState(self.win,0,'_NET_WM_STATE_MAXIMIZED_HORZ')
        self.info.ewmh.setWmState(self.win,0,'_NET_WM_STATE_MAXIMIZED_VERT')
        self.info.ewmh.setWmState(self.win,0,'_NET_WM_STATE_FULLSCREEN')
        self.info.ewmh.setWmState(self.win,1,'_NET_WM_STATE_DEMANDS_ATTENTION')
        self.info.ewmh.setMoveResizeWindow(self.win,
                                  x=self.x, y=self.y,\
                                  w=self.w, h=self.h)
        self.info.ewmh.display.flush()