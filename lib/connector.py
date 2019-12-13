from io import BytesIO

from PIL import Image

from lib.utils import Utils

class Connector:
	dates_url = ""
	images_url = ""
	source_name = ""
	sources = {}
	last_download = None

	def __init__(self, source_name):
		self.source_name = source_name

	def get_image_info(self):
		raise NotImplementedError

	def get_image(self):
		image_info = self.get_image_info()
		if self.last_download == image_info["latest_date"]:
			return False
		self.last_download = image_info["latest_date"]

		image_blob_tab = []
		for y in range(len(image_info["url_tab"])):
			image_blob_tab.append([])
			for x in range(len(image_info["url_tab"][0])):
				image_blob_tab[y].append(Utils.http_request(image_info["url_tab"][y][x]))

		full_image = self.append_image(image_blob_tab, image_info)
		image_path = Utils.get_image_path()
		full_image.save(image_path)
		return image_path

	@staticmethod
	def append_image(image_tab, image_info):
		for y in range(len(image_tab)):
			for x in range(len(image_tab[0])):
				image_tab[y][x] = Image.open(BytesIO(image_tab[y][x]))

		full_image = Image.new(
			"RGB",
			(
				image_tab[0][0].size[0] * len(image_tab[0]),
				image_tab[0][0].size[1] * len(image_tab)
			)
		)

		for y in range(len(image_tab)):
			for x in range(len(image_tab[0])):
				full_image.paste(image_tab[y][x], (image_tab[0][0].size[0]*x, image_tab[0][0].size[1]*y))


		return full_image

		# Need to add crop + resizing
		if "offset_x" in image_info:
			max_width = full_image.size[0]-image_info["offset_x"]
			if max_width>Utils.get_screen_size()["width"]:
				max_width = Utils.get_screen_size()["width"]
			full_image = full_image.crop(
				(
					image_info["offset_x"],
					0,
					max_width+image_info["offset_x"],
					full_image.size[1],
				)
			)
			Utils.get_screen_size()["width"]

		if "offset_y" in image_info:
			max_height = full_image.size[1]-image_info["offset_y"]
			if max_height>Utils.get_screen_size()["height"]:
				max_height = Utils.get_screen_size()["height"]
			full_image = full_image.crop(
				(
					0,
					image_info["offset_y"],
					full_image.size[0],
					max_height+image_info["offset_y"],
				)
			)

		return full_image
