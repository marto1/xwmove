from ewmh import EWMH
import posinfo


class Window:
    """
    Window representation.
    """

    def __init__(self, win=None, x=0, y=0, w=1, h=1,gravity = 0):

        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.win = win
        self.gravity = gravity

    def __eq__(self, other):
        """
        Take notice that win is NOT included in the comparison.
        """

        if ((self.x == other.x) and
            (self.y == other.y) and
            (self.w == other.w) and
            (self.h == other.h)):

            return True
        else:
            return False

    def __ne__(self, other):
        """
        Take notice that win is NOT included in the comparison.
        """

        if ((self.x == other.x) and
            (self.y == other.y) and
            (self.w == other.w) and
            (self.h == other.h)):

            return False
        else:
            return True

    def as_tuple(self):
        """
        Represent the object as a tuple.
        """
        return (self.win, self.gravity, self.x, self.y, self.w, self.h)


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

        if (where == 'center' and size == 'full'):
            self._maximize()
            return

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
    def _maximize(self):
        """
        Maximize the window.
        """
        self.info.ewmh.setWmState(self.win,1,'_NET_WM_STATE_MAXIMIZED_HORZ')
        self.info.ewmh.setWmState(self.win,1,'_NET_WM_STATE_MAXIMIZED_VERT')
        self.info.ewmh.setMoveResizeWindow(self.win,
                                  x=self.info.topX, y=self.info.topY,\
                                  w=self.info.FULL_W, h=self.info.FULL_H)
        self.info.ewmh.display.flush()

class DispatchMove(WindowMove):
    """
    Makes the decision how the window has to be moved.
    """

    def __init__(self, info, doubleMode = False):
        WindowMove.__init__(self, info)
        self.currentWindow = None
        self.doubleMode = doubleMode

    def move(self, window, where = 'center'):

        self.currentWindow = Window(window,
                            *self._get_current_window_geometry(window))

        print self.currentWindow.as_tuple()

        if (not self.doubleMode):
            WindowMove.move(self,window,where,'half')
            return

        self.center = Window(x=self.info.QUARTER_W, y = self.info.QUARTER_H,
                             w=self.info.HALF_W, h= self.info.HALF_H)

        if ((where == 'center') and (self.center == self.currentWindow)):
            WindowMove.move(self,window,where,'full')
            return
        else:
            WindowMove.move(self,window,where,'half')
            return

    def _get_current_window_geometry(self,window):
        """
        Get list with the x,y,w,h of the current window.
        Note: Window.get_geometry() gives relative pos information for x and y
        so external call to xwininfo is needed.
        """
        import commands
        output = commands.getoutput("xwininfo -id " + str(window.id))
        x=y=0
        for item in output.split("\n"):
            if "Absolute upper-left X" in item:
                x = item.strip()
            if "Absolute upper-left Y" in item:
                y = item.strip()

        x = [int(s) for s in x.split() if s.isdigit()][0]
        y = [int(s) for s in y.split() if s.isdigit()][0]
        w=window.get_geometry()._data['width']
        h=window.get_geometry()._data['height']
        return (x,y,w,h)