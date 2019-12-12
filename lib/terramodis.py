import math
from datetime import datetime, timedelta

from lib.utils import Utils
from lib.connector import Connector


class Terramodis(Connector):
	cooldown = 60 * 60 * 1
	zone_tile = {
		"europe": {
			"start_tile_x": 18,
			"start_tile_y": 4,
			"zoom_level": 5,
			"offset_x": 400,
			"offset_y": 0
		}
	}
	tile_size = {
		"width": 512,
		"height": 512,
	}
	images_url = (
		"https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/MODIS_Terra_CorrectedReflectance_TrueColor"
		"/default/{Time}/{TileMatrixSet}/{ZoomLevel}/{TileRow}/{TileCol}.jpg"
	)

	def get_image_info(self):
		latest_date = datetime.utcnow() + timedelta(days=-1)
		img_url_template = self.images_url.format(
			Time=latest_date.strftime("%Y-%m-%d"),
			TileMatrixSet="250m",
			ZoomLevel=self.zone_tile[self.connector_name]["zoom_level"],
			TileRow="{TileRow}",
			TileCol="{TileCol}",
		)


		tile_x = math.ceil((Utils.get_screen_size()["width"]+self.zone_tile[self.connector_name]["offset_x"])/self.tile_size["width"])
		tile_y = math.ceil((Utils.get_screen_size()["height"]+self.zone_tile[self.connector_name]["offset_y"])/self.tile_size["height"])

		url_tab = []
		for y in range(tile_y):
			url_tab.append([])
			for x in range(tile_x):
				url_tab[y].append(
					img_url_template.format(
						TileCol=x+self.zone_tile[self.connector_name]["start_tile_x"],
						TileRow=y+self.zone_tile[self.connector_name]["start_tile_y"],
					)
				)

		return {
			"latest_date": latest_date,
			"url_tab": url_tab,
			**self.zone_tile[self.connector_name]
		}


#Doc API : https://wiki.earthdata.nasa.gov/display/GIBS/GIBS+API+for+Developers
