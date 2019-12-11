from io import BytesIO

from PIL import Image

from lib.utils import Utils


class Connector:
    dates_url = ""
    images_url = ""
    cooldown = 60 * 10
    last_download = None

    def get_image_link(self):
        raise NotImplementedError

    def get_image(self):
        return self.get_full_disk_image()

    def get_full_disk_image(self):
        image_link = self.get_image_link()
        if self.last_download == image_link[0]:
            return False
        self.last_download = image_link[0]

        image_url_tab = image_link[1]
        image_blob_tab = []
        for url in image_url_tab:
            image_blob_tab.append(Utils.http_request(url))
        full_disk_image = self.append_full_disk_image(image_blob_tab)

        image_path = Utils.get_image_path()
        full_disk_image.save(image_path)
        return image_path

    @staticmethod
    def append_full_disk_image(image_blob_tab):
        image_tab = []
        for blob in image_blob_tab:
            image_tab.append(Image.open(BytesIO(blob)))

        full_disk_image = Image.new(
            "RGB",
            (
                image_tab[0].size[0] + image_tab[1].size[0],
                image_tab[0].size[1] + image_tab[2].size[1],
            ),
        )

        full_disk_image.paste(image_tab[0], (0, 0))
        full_disk_image.paste(image_tab[1], (image_tab[0].size[0], 0))
        full_disk_image.paste(image_tab[2], (0, image_tab[0].size[1]))
        full_disk_image.paste(
            image_tab[3], (image_tab[0].size[0], image_tab[0].size[1])
        )

        return full_disk_image
