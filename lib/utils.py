import json
import os
import re
import time
import urllib.request as urllib


class Utils:
	save_path = os.path.expanduser("~/StrobeBackground") + "/"
	image_name = "background.png"
	screen_size = {
		"width": 1920,
		"height": 1080,
	}

	@staticmethod
	def http_request(url, retry=3, sleep=60):
		while True:
			if retry == 0:
				raise TimeoutError("Utils.http_request timeout")
			try:
				data = urllib.urlopen(url).read()
				break
			except Exception as err:
				print("Exception:", err)
				retry -= 1
				time.sleep(sleep)
		return data

	@staticmethod
	def http_request_json(url, retry=3, sleep=60):
		http_data = Utils.http_request(url, retry, sleep)
		json_data = json.loads(http_data.decode("utf-8"))
		return json_data

	@staticmethod
	def get_image_path():
		if not os.path.exists(Utils.save_path):
			os.makedirs(Utils.save_path)
		return Utils.save_path + Utils.image_name

	@staticmethod
	def background_image_exists():
		return os.path.exists(Utils.get_image_path())

	@staticmethod
	def set_screen_size(max_size):
		max_size = str(max_size).lower()
		reg = re.compile('^\d{1,4}x\d{1,4}$')
		if reg.match(max_size) == None:
			return
		s_size = max_size.split("x")
		Utils.screen_size["width"] = int(s_size[0])
		Utils.screen_size["height"] = int(s_size[1])

	@staticmethod
	def get_screen_size():
		return Utils.screen_size
