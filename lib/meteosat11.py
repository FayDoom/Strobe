from lib.utils import Utils
from io import BytesIO
from PIL import Image
import sys


class Meteosat11:

	cooldown	  = 60*15
	datesUrl      = "https://rammb-slider.cira.colostate.edu/data/json/meteosat-11/full_disk/natural_color/latest_times.json"
	earthImgUrl   = "https://rammb-slider.cira.colostate.edu/data/imagery/{date}/meteosat-11---full_disk/natural_color/{datetime}/01/{imgname}.png"

	def __init_(self):
		pass

	def getImage(self):
		return self.getFullDiskImg()

	def getImgLink(self):
		latestDate = Utils.httpRequestJson(self.datesUrl)["timestamps_int"][0]
		imgUrlTemplate = self.earthImgUrl.format(
			date     = str(latestDate)[0:8],
			datetime = latestDate,
			imgname  = '{imgname}'
		)
		imgUrlTab = [];
		for s in ['000_000', '000_001', '001_000', '001_001']:
			imgUrlTab.append(imgUrlTemplate.format(imgname=s))
		return [latestDate, imgUrlTab]

	def getFullDiskImg(self):
		imgLink    = self.getImgLink()
		imgUrlTab  = imgLink[1]
		imgBlobTab = [];
		for url in imgUrlTab:
			imgBlobTab.append(Utils.httpRequest(url))
		fullDiskImg = self.appendFullDiskImg(imgBlobTab)

		imgPath = Utils.getImagePath()+'background.png'
		fullDiskImg.save(imgPath)
		return imgPath

	def appendFullDiskImg(self, imgBlobTab):
		imgTab = []
		for blob in imgBlobTab:
			imgTab.append(Image.open(BytesIO(blob)))

		fullDiskImg = Image.new('RGB', (
			imgTab[0].size[0] + imgTab[1].size[0],
			imgTab[0].size[1] + imgTab[2].size[1]
		))

		fullDiskImg.paste(imgTab[0], (0, 0))
		fullDiskImg.paste(imgTab[1], (imgTab[0].size[0], 0))
		fullDiskImg.paste(imgTab[2], (0, imgTab[0].size[1]))
		fullDiskImg.paste(imgTab[3], (imgTab[0].size[0], imgTab[0].size[1]))

		return fullDiskImg
