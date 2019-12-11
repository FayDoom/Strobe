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

    def get_image_link(self):
        latest_date = Utils.http_request_json(self.dates_url)["date"]
        date_obj = datetime.datetime.strptime(latest_date, "%Y-%m-%d %H:%M:%S")
        img_url_template = self.images_url.format(
            y=date_obj.strftime("%Y"),
            m=date_obj.strftime("%m"),
            d=date_obj.strftime("%d"),
            image_name="{image_name}",
        )
        img_url_tab = []
        for s in ["0_0", "1_0", "0_1", "1_1"]:
            img_url_tab.append(
                img_url_template.format(
                    image_name=date_obj.strftime("%H%M%S") + "_" + s
                )
            )
        return [latest_date, img_url_tab]
