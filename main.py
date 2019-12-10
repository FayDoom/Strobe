from lib.meteosat11 import Meteosat11
from lib.utils import Utils
import time
import ctypes
import sys
import os


class Strobe:

	imageGetter = None

	def __init_(self, imageGetter):
		self.imageGetter = imageGetter
		self.initTimeLoop()

	def initTimeLoop(self):
		retry = 0
		while True:
			if retry==4: break
			try:
				self.imageGetter.getImage()
				retry = 0
			except Exception as err:
				print("Error :", err, sys.exc_info()[0])
				++retry
			time.sleep(self.imageGetter.cooldown)

	def setBackground(imagePath):
		ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath , 0)



Strobe()
