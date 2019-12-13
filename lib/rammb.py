from lib.utils import Utils
from lib.connector import Connector


class Rammb(Connector):
	dates_url = (
		"https://rammb-slider.cira.colostate.edu/data/json/{satname}/"
		"full_disk/geocolor/latest_times.json"
	)
	images_url = (
		"https://rammb-slider.cira.colostate.edu/data/imagery/{date}/"
		"{satname}---full_disk/geocolor/{datetime}/0{zoomlevel}/{imagename}.png"
	)

	def get_image_info(self):
		src_info = self.sources[self.source_name]

		latest_date = Utils.http_request_json(
			self.dates_url.format(satname=src_info["satname"])
		)["timestamps_int"][0]

		img_url_template = self.images_url.format(
			date=str(latest_date)[0:8],
			datetime=latest_date,
			zoomlevel=src_info["zoom_level"],
			satname=src_info["satname"],
			imagename="{imagename}",
		)

		url_tab = []
		for y in range(self.sources[self.source_name]["tile_x"]):
			url_tab.append([])
			for x in range(self.sources[self.source_name]["tile_y"]):
				url_tab[y].append(
					img_url_template.format(imagename="0"*(3-len(str(y)))+str(y)+"_"+"0"*(3-len(str(x)))+str(x))
				)

		return {
			"latest_date": latest_date,
			"url_tab": url_tab,
			**self.sources[self.source_name]
		}


	sources = {
		"meteosat8": {
			"satname": "meteosat-8",
			"cooldown": 60 * 15,
			"zoom_level": 1,
			"start_tile_x": 0,
			"start_tile_y": 0,
			"tile_x": 2,
			"tile_y": 2,
			"offset_x": 0,
			"offset_y": 0
		},
		"meteosat11": {
			"satname": "meteosat-11",
			"cooldown": 60 * 15,
			"zoom_level": 1,
			"start_tile_x": 0,
			"start_tile_y": 0,
			"tile_x": 2,
			"tile_y": 2,
			"offset_x": 0,
			"offset_y": 0
		},
		"himawari8": {
			"satname": "himawari",
			"cooldown": 60 * 10,
			"zoom_level": 1,
			"start_tile_x": 0,
			"start_tile_y": 0,
			"tile_x": 2,
			"tile_y": 2,
			"offset_x": 0,
			"offset_y": 0
		},
		"goes16": {
			"satname": "goes-16",
			"cooldown": 60 * 10,
			"zoom_level": 1,
			"start_tile_x": 0,
			"start_tile_y": 0,
			"tile_x": 2,
			"tile_y": 2,
			"offset_x": 0,
			"offset_y": 0
		},
		"goes17": {
			"satname": "goes-17",
			"cooldown": 60 * 10,
			"zoom_level": 1,
			"start_tile_x": 0,
			"start_tile_y": 0,
			"tile_x": 2,
			"tile_y": 2,
			"offset_x": 0,
			"offset_y": 0
		},
	}
