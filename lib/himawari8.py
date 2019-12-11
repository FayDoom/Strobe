import datetime
from io import BytesIO

from PIL import Image

from lib.utils import Utils


class Himawari8:
    cooldown = 60 * 10
    datesUrl = "http://himawari8-dl.nict.go.jp/himawari8/img/D531106/latest.json"
    earthImgUrl = "https://himawari8-dl.nict.go.jp/himawari8/img/D531106/2d/550/{y}/{m}/{d}/{imgname}.png"
    lastDownload = None

    def __init_(self):
        pass

    def getImage(self):
        return self.getFullDiskImg()

    def getImgLink(self):
        latestDate = Utils.httpRequestJson(self.datesUrl)["date"]
        dateObj = datetime.datetime.strptime(latestDate, "%Y-%m-%d %H:%M:%S")
        imgUrlTemplate = self.earthImgUrl.format(
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

    def getFullDiskImg(self):
        imgLink = self.getImgLink()
        if self.lastDownload == imgLink[0]:
            return False
        self.lastDownload = imgLink[0]

        imgUrlTab = imgLink[1]
        imgBlobTab = []
        for url in imgUrlTab:
            imgBlobTab.append(Utils.httpRequest(url))
        fullDiskImg = self.appendFullDiskImg(imgBlobTab)

        imgPath = Utils.getImagePath()
        fullDiskImg.save(imgPath)
        return imgPath

    def appendFullDiskImg(self, imgBlobTab):
        imgTab = []
        for blob in imgBlobTab:
            imgTab.append(Image.open(BytesIO(blob)))

        fullDiskImg = Image.new(
            "RGB",
            (
                imgTab[0].size[0] + imgTab[1].size[0],
                imgTab[0].size[1] + imgTab[2].size[1],
            ),
        )

        fullDiskImg.paste(imgTab[0], (0, 0))
        fullDiskImg.paste(imgTab[1], (imgTab[0].size[0], 0))
        fullDiskImg.paste(imgTab[2], (0, imgTab[0].size[1]))
        fullDiskImg.paste(imgTab[3], (imgTab[0].size[0], imgTab[0].size[1]))

        return fullDiskImg
