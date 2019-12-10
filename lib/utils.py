import urllib
import json
import time
import os


class Utils:

	savePath = os.path.expanduser('~/StrobeBackground')

	@staticmethod
	def httpRequest(url, retry=3, sleep=60):
		while True:
			if retry==0: raise TimeoutError('Utils.httpRequest timeout')
			try:
				data = urllib.request.urlopen(url).read()
				break
			except urllib.error.HTTPError as err:
				retry-=1
				time.sleep(sleep)
		return data

	@staticmethod
	def httpRequestJson(url, retry=3, sleep=60):
		httpData = Utils.httpRequest(url, retry, sleep)
		jsonData = json.loads(httpData.decode('utf-8'))
		return jsonData

	@staticmethod
	def getImagePath(subFolder):
		path = Utils.savePath+'/'+subFolder+'/'
		if not os.path.exists(Utils.savePath): os.makedirs(Utils.savePath)
		if not os.path.exists(path): os.makedirs(path)
		return path
