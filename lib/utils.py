import urllib.request as urllib
import os
import json
import time


class Utils:

	savePath  = os.path.expanduser('~/StrobeBackground')+'/'
	imageName = 'background.png'

	@staticmethod
	def httpRequest(url, retry=3, sleep=60):
		while True:
			if retry==0: raise TimeoutError('Utils.httpRequest timeout')
			try:
				data = urllib.urlopen(url).read()
				break
			except Exception as err:
				retry-=1
				time.sleep(sleep)
		return data

	@staticmethod
	def httpRequestJson(url, retry=3, sleep=60):
		httpData = Utils.httpRequest(url, retry, sleep)
		jsonData = json.loads(httpData.decode('utf-8'))
		return jsonData

	@staticmethod
	def getImagePath():
		if not os.path.exists(Utils.savePath): os.makedirs(Utils.savePath)
		return Utils.savePath+Utils.imageName

	@staticmethod
	def isBackgroundImgExist():
		return os.path.exists(Utils.getImagePath())
