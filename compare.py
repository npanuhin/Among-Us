from fuzzywuzzy import fuzz
from PIL import Image


class ImageCompare:
    def __init__(self):
        self.buffer = {}

    def compare(self, image1, image2, crop=None, resize=(8, 8), bw_threshold=None):

        if isinstance(image1, str):
            if image2 not in self.buffer:
                self.buffer[image2] = Image.open(image2)

            image2 = self.buffer[image2]

        if isinstance(image2, str):
            if image2 not in self.buffer:
                self.buffer[image2] = Image.open(image2)

            image2 = self.buffer[image2]

        if crop is not None:
            image1 = image1.crop(crop)
            image2 = image2.crop(crop)

        image1 = image1.resize(resize, Image.NEAREST).convert('L')
        image2 = image2.resize(resize, Image.NEAREST).convert('L')

        pixel_data = list(image1.getdata())
        if bw_threshold is None:
            avg_pixel = sum(pixel_data) / len(pixel_data)
        else:
            # image1.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data)
        image1_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

        pixel_data = list(image2.getdata())
        if bw_threshold is None:
            avg_pixel = sum(pixel_data) / len(pixel_data)
        else:
            # image2.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data)
        image2_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

        # image1.show()
        # image2.show()

        # print(image1_hash)
        # print()
        # print(image2_hash)
        # print(fuzz.ratio(image1_hash, image2_hash))

        # if len(image1_hash) >= len(image2_hash):
        #     result = min(
        #         sum(abs(ord(image1_hash[start + i]) - ord(image2_hash[i])) for i in range(len(image2_hash)))
        #         for start in range(len(image1_hash) - len(image2_hash) + 1)
        #     )
        # else:
        #     result = min(
        #         sum(abs(ord(image1_hash[i]) - ord(image2_hash[start + i])) for i in range(len(image1_hash)))
        #         for start in range(len(image2_hash) - len(image1_hash) + 1)
        #     )

        # image1.show()
        # image1.save("result.png")

        image1.close()
        image2.close()

        return fuzz.ratio(image1_hash, image2_hash)
