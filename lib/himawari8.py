import datetime

from lib.utils import Utils
from lib.connector import Connector


class Himawari8(Connector):
    cooldown = 60 * 10
    dates_url = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    images_url = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/{y}/{m}/{d}/{imgname}.png"
    last_download = None

    def getImgLink(self):
        latestDate = Utils.httpRequestJson(self.dates_url)["date"]
        dateObj = datetime.datetime.strptime(latestDate, "%Y-%m-%d %H:%M:%S")
        imgUrlTemplate = self.images_url.format(
            y=dateObj.strftime("%Y"),
            m=dateObj.strftime("%m"),
            d=dateObj.strftime("%d"),
            imgname="{imgname}",
        )
        imgUrlTab = []
        for s in ["0_0", "1_0", "0_1", "1_1"]:
            imgUrlTab.append(
                imgUrlTemplate.format(imgname=dateObj.strftime("%H%M%S") + "_" + s)
            )
        return [latestDate, imgUrlTab]
