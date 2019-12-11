import ctypes
import sys
import time
from ctypes import wintypes

from lib.himawari8 import Himawari8
from lib.meteosat11 import Meteosat11
from lib.utils import Utils


class Strobe:
    imgConnector = None

    def __init__(self, connectorName):
        self.setDefaultBackground()
        self.initConnector(connectorName)
        self.initTimeLoop()

    def initConnector(self, connectorName):
        switch = {"meteosat11": Meteosat11, "himawari8": Himawari8}
        connector = switch.get(connectorName.lower().replace("-", ""), 'meteosat11')
        self.imgConnector = connector()

    def initTimeLoop(self):
        retry = 0
        while True:
            if retry == 5:
                break
            try:
                imgPath = self.imgConnector.getImage()
                if imgPath == False:
                    continue
                self.setBackground(imgPath)
                retry = 0
            except Exception as err:
                print("Error :", err, sys.exc_info()[0])
                retry += 1
            time.sleep(self.imgConnector.cooldown)

    def setBackground(self, imgPath):
        ctypes.WinDLL("user32").SystemParametersInfoW(20, 0, imgPath, 0)

    def setDefaultBackground(self):
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x0001
        SPIF_SENDWININICHANGE = 0x0002
        SystemParametersInfo = ctypes.WinDLL("user32").SystemParametersInfoW
        SystemParametersInfo.argtypes = (
            ctypes.c_uint,
            ctypes.c_uint,
            ctypes.c_void_p,
            ctypes.c_uint,
        )
        SystemParametersInfo.restype = wintypes.BOOL
        SystemParametersInfo(
            SPI_SETDESKWALLPAPER,
            0,
            Utils.getImagePath(),
            SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
        )
