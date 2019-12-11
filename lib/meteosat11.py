from lib.utils import Utils
from lib.connector import Connector


class Meteosat11(Connector):
    cooldown = 60 * 15
    dates_url = "https://rammb-slider.cira.colostate.edu/data/json/meteosat-11/full_disk/natural_color/latest_times.json"
    images_url = "https://rammb-slider.cira.colostate.edu/data/imagery/{date}/meteosat-11---full_disk/natural_color/{datetime}/01/{imgname}.png"
    last_download = None

    def getImgLink(self):
        latestDate = Utils.httpRequestJson(self.dates_url)["timestamps_int"][0]
        imgUrlTemplate = self.images_url.format(
            date=str(latestDate)[0:8], datetime=latestDate, imgname="{imgname}"
        )
        imgUrlTab = []
        for s in ["000_000", "000_001", "001_000", "001_001"]:
            imgUrlTab.append(imgUrlTemplate.format(imgname=s))
        return [latestDate, imgUrlTab]
