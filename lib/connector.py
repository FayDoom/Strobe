from io import BytesIO

from PIL import Image

from lib.utils import Utils


class Connector:
    def __init_(self, dates_url, images_url):
        self.dates_url = dates_url
        self.images_url = images_url
        self.cooldown = 60 * 10
        self.last_download = None

    def __init_(self):
        pass

    def getImgLink(self):
        raise NotImplementedError

    def getImage(self):
        return self.getFullDiskImg()

    def getFullDiskImg(self):
        imgLink = self.getImgLink()
        if self.last_download == imgLink[0]:
            return False
        self.last_download = imgLink[0]

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
