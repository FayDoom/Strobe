import ctypes
import os
import sys
import time
import pkgutil
import importlib
from subprocess import call

from lib.connector import Connector
from lib.utils import Utils

try:
	from ctypes import wintypes
except ValueError:
	pass


class Strobe:
	default_source = "meteosat11"
	connector_list = {}
	connector = None
	cooldown = 60 * 30

	def __init__(self, source_name, platform):
		self.changer = "/usr/bin/Esetroot"
		self.display = ":0.0"
		self.scaling = "-fit"  # None=off, '-scale', '-fit'
		self.source_name = source_name.lower().replace("-", "")

		self.platform = platform

		if platform in ("linux", "freebsd") and not os.path.exists(self.changer):
			print(
				"You will need to install esetroot at /usr/bin/Esetroot for "
				"this to work on linux or freebsd."
			)

		self.set_default_background()
		self.import_connecter()
		self.init_connector()
		self.init_time_loop()

	def init_connector(self):
		for c in self.connector_list:
			if self.source_name in self.connector_list[c].sources.keys():
				self.connector = self.connector_list[c](self.source_name)
				return
		self.source_name = self.default_source
		self.init_connector()

	def import_connecter(self):
		dir = os.path.dirname(__file__)
		for (module_loader, name, ispkg) in pkgutil.iter_modules([dir]):
			importlib.import_module('.' + name, __package__)
		self.connector_list = {cls.__name__: cls for cls in Connector.__subclasses__()}

	def init_time_loop(self):
		retry = 0
		while True:
			if retry == 5:
				break
			try:
				image_path = self.connector.get_image()
				if not image_path:
					continue
				self.set_background(image_path)
				retry = 0
			except Exception as err:
				print("Error :", err, sys.exc_info()[0])
				retry += 1
			print("Sleep for "+str(self.connector.sources[self.source_name]["cooldown"])+"s")
			time.sleep(self.connector.sources[self.source_name]["cooldown"])

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
