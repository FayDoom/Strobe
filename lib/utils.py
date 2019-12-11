import json
import os
import time
import urllib.request as urllib


class Utils:
    save_path = os.path.expanduser("~/StrobeBackground") + "/"
    image_name = "background.png"

    @staticmethod
    def http_request(url, retry=3, sleep=60):
        while True:
            if retry == 0:
                raise TimeoutError("Utils.http_request timeout")
            try:
                data = urllib.urlopen(url).read()
                break
            except Exception as err:
                print("Exception:", err)
                retry -= 1
                time.sleep(sleep)
        return data

    @staticmethod
    def http_request_json(url, retry=3, sleep=60):
        http_data = Utils.http_request(url, retry, sleep)
        json_data = json.loads(http_data.decode("utf-8"))
        return json_data

    @staticmethod
    def get_image_path():
        if not os.path.exists(Utils.save_path):
            os.makedirs(Utils.save_path)
        return Utils.save_path + Utils.image_name

    @staticmethod
    def background_image_exists():
        return os.path.exists(Utils.get_image_path())
