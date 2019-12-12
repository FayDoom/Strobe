import datetime

from lib.utils import Utils
from lib.connector import Connector


class Himawari8(Connector):
	cooldown = 60 * 10
	dates_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
	images_url = (
		"https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550"
		"/{y}/{m}/{d}/{image_name}.png"
	)

	def get_image_info(self):
		latest_date = Utils.http_request_json(self.dates_url)["date"]
		date_obj = datetime.datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
		image_url_template = self.images_url.format(
			y=date_obj.strftime("%Y"),
			m=date_obj.strftime("%m"),
			d=date_obj.strftime("%d"),
			image_name="{image_name}",
		)

		time_str = date_obj.strftime("%H%M%S")
		url_tab = [
			[
				image_url_template.format(image_name=time_str+"_0_0"),
					image_url_template.format(image_name=time_str+"_1_0")
			],
			[
				image_url_template.format(image_name=time_str+"_0_1"),
				image_url_template.format(image_name=time_str+"_1_1")
			],
		]

		return {
			"latest_date": latest_date,
			"url_tab": url_tab,
		}
