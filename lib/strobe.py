from lib.meteosat11 import Meteosat11
from lib.utils import Utils
import time
import ctypes
import sys


class Strobe:

	imgConnecter = None

	def __init__(self, connecterName):
		self.initConnecter(connecterName)
		self.initTimeLoop()

	def initConnecter(self, connecterName):
		switch = { "meteosat11" : Meteosat11 }
		object = switch.get(connecterName.lower(), Meteosat11)
		self.imgConnecter = object()

	def initTimeLoop(self):
		retry = 0
		while True:
			if retry==5: break
			try:
				imgPath = self.imgConnecter.getImage()
				if imgPath==False: continue
				print("New image ->", imgPath)
				self.setBackground(imgPath)
				retry = 0
			except Exception as err:
				print("Error :", err, sys.exc_info()[0])
				retry+=1
			time.sleep(self.imgConnecter.cooldown)

	def setBackground(self, imgPath):
		ctypes.windll.user32.SystemParametersInfoW(20, 0, imgPath , 0)
