import ctypes
import os
import sys
import time
from subprocess import call

from lib.himawari8 import Himawari8
from lib.meteosat11 import Meteosat11
from lib.terramodis import Terramodis
from lib.utils import Utils

try:
	from ctypes import wintypes
except ValueError:
	pass


class Strobe:
	image_connector = None

	def __init__(self, connector_name, platform):
		self.changer = "/usr/bin/Esetroot"
		self.display = ":0.0"
		self.scaling = "-fit"  # None=off, '-scale', '-fit'

		self.platform = platform

		if platform in ("linux", "freebsd") and not os.path.exists(self.changer):
			print(
				"You will need to install esetroot at /usr/bin/Esetroot for "
				"this to work on linux or freebsd."
			)

		self.set_default_background()
		self.init_connector(connector_name)
		self.init_time_loop()

	def init_connector(self, connector_name):
		connector_name = connector_name.lower().replace("-", "")
		switch = {"meteosat11": Meteosat11, "himawari8": Himawari8, "europe": Terramodis}
		if not connector_name in switch:
			connector_name = "meteosat11"
		connector = switch.get(connector_name)
		self.image_connector = connector(connector_name)

	def init_time_loop(self):
		retry = 0
		while True:
			if retry == 5:
				break
			try:
				image_path = self.image_connector.get_image()
				if not image_path:
					continue
				self.set_background(image_path)
				retry = 0
			except Exception as err:
				print("Error :", err, sys.exc_info()[0])
				retry += 1
			time.sleep(self.image_connector.cooldown)

	def set_background(self, image_path):
		if self.platform in ("linux", "freebsd"):
			self._set_background_linux(image_path)
		elif self.platform in "windows":
			self._set_background_windows(image_path)

	def _set_background_linux(self, image_path):
		change_command = [self.changer, "-d", self.display, image_path]
		if self.scaling is not None:
			change_command.insert(1, self.scaling)
		print("Calling '%s'", change_command)
		call(change_command)

	@staticmethod
	def _set_background_windows(image_path):
		ctypes.WinDLL("user32").SystemParametersInfoW(20, 0, image_path, 0)

	def set_default_background(self):
		if self.platform in ("linux", "freebsd"):
			self._set_default_background_linux()
		elif self.platform in "windows":
			self._set_default_background_windows()

	def _set_default_background_linux(self):
		self._set_background_linux(Utils.get_image_path())

	# noinspection PyPep8Naming
	@staticmethod
	def _set_default_background_windows():
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
			Utils.get_image_path(),
			SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE,
		)
