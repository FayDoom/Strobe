from lib.utils import Utils
from lib.connector import Connector


class Meteosat11(Connector):
    cooldown = 60 * 15
    dates_url = (
        "https://rammb-slider.cira.colostate.edu/data/json/meteosat-11/"
        "full_disk/natural_color/latest_times.json"
    )
    images_url = (
        "https://rammb-slider.cira.colostate.edu/data/imagery/{date}/"
        "meteosat-11---full_disk/natural_color/{datetime}/01/{image_name}.png"
    )

    def get_image_link(self):
        latest_date = Utils.http_request_json(self.dates_url)["timestamps_int"][0]
        image_url_template = self.images_url.format(
            date=str(latest_date)[0:8], datetime=latest_date, image_name="{image_name}"
        )
        img_url_tab = []
        for s in ["000_000", "000_001", "001_000", "001_001"]:
            img_url_tab.append(image_url_template.format(image_name=s))
        return [latest_date, img_url_tab]
