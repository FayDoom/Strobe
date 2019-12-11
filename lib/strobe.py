from lib.meteosat11 import Meteosat11
from lib.himawari8 import Himawari8
from lib.utils import Utils
from ctypes import wintypes
import ctypes
import time
import sys


class Strobe:

	imgConnecter = None

	def __init__(self, connecterName):
		self.setDefaultBackground()
		self.initConnecter(connecterName)
		self.initTimeLoop()

	def initConnecter(self, connecterName):
		switch = { "meteosat11" : Meteosat11, "himawari8" : Himawari8 }
		object = switch.get(connecterName.lower().replace("-", ""), Meteosat11)
		self.imgConnecter = object()

	def initTimeLoop(self):
		retry = 0
		while True:
			if retry==5: break
			try:
				imgPath = self.imgConnecter.getImage()
				if imgPath==False: continue
				self.setBackground(imgPath)
				retry = 0
			except Exception as err:
				print("Error :", err, sys.exc_info()[0])
				retry+=1
			time.sleep(self.imgConnecter.cooldown)

	def setBackground(self, imgPath):
		ctypes.WinDLL('user32').SystemParametersInfoW(20, 0, imgPath , 0)

	def setDefaultBackground(self):
		SPI_SETDESKWALLPAPER  = 0x0014
		SPIF_UPDATEINIFILE    = 0x0001
		SPIF_SENDWININICHANGE = 0x0002
		SystemParametersInfo          = ctypes.WinDLL('user32').SystemParametersInfoW
		SystemParametersInfo.argtypes = ctypes.c_uint,ctypes.c_uint,ctypes.c_void_p,ctypes.c_uint
		SystemParametersInfo.restype  = wintypes.BOOL
		SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, Utils.getImagePath(), SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE)
