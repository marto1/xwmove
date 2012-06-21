from ewmh import EWMH
import config

class MainInfo:
    """
    Get information about the work area,
    absolute positions for the SPECIAL* places
    and widths and heights for the same

    * - middle,right top corner,left bottom corner etc.
    """
    def __init__(self,ewmh):

        self.ewmh = ewmh
        self.currentDesktop = self.ewmh.getCurrentDesktop()
        workArea = ewmh.getWorkArea()

        self.topX = workArea[0 + 4*self.currentDesktop] + config.LEFT_FIX
        self.topY = workArea[1 + 4*self.currentDesktop] + config.TOP_FIX
        self.mainW = workArea[2 + 4*self.currentDesktop]
        self.mainH  = workArea[3 + 4*self.currentDesktop]

        self.FULL_W = self.mainW - config.LEFT_FIX
        self.FULL_H = self.mainH - config.TOP_FIX

        self.HALF_W = self.mainW/2
        self.HALF_H = self.mainH/2

        self.QUARTER_W = self.mainW/4
        self.QUARTER_H = self.mainH/4

        self.topRightHalfX = self.HALF_W + config.TOP_FIX
        self.topRightQuarterX = self.QUARTER_W * 3

        self.bottomLeftY = self.HALF_H + config.TOP_FIX + config.BOTTOM_FIX


