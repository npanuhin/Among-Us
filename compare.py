from fuzzywuzzy import fuzz
from PIL import Image


class ImageCompare:
    def __init__(self):
        self.buffer = {
            # [
            #     full_image,
            #     {
            #         hash(tuple(crop)): {
            #             image,
            #             {
            #                 hash(tuple(resize)): image.convert('L')
            #             }
            #         }
            #     }
            # ]
        }

    def save_image(self, path):
        if path not in self.buffer:
            self.buffer[path] = [Image.open(path), {}]

        return self.buffer[path]

    def save_modified_image(self, path, crop, resize):
        if hash(tuple(crop + resize)) not in self.buffer[path][1]:
            self.buffer[path][1][hash(tuple(crop + resize))] = list(
                self.buffer[path][0].crop(crop).resize(resize, Image.NEAREST).convert('L').getdata()
            )

        return self.buffer[path][1][hash(tuple(crop + resize))]

    def compare(self, image1, image2, crop=None, resize=[16, 16], bw_threshold=None):
        # print(crop, tuple(crop), hash(tuple(crop)))
        # print(self.buffer)

        if not isinstance(image1, str):
            if crop is not None:
                image1 = image1.crop(crop)
            pixel_data_image1 = list(image1.resize(resize, Image.NEAREST).convert('L').getdata())

        else:
            self.save_image(image1)

            if crop is None:
                pixel_data_image1 = list(self.buffer[image1][0].resize(resize, Image.NEAREST).convert('L').getdata())
            else:
                pixel_data_image1 = self.save_modified_image(image1, crop, resize)

        if not isinstance(image2, str):
            if crop is not None:
                image2 = image2.crop(crop)
            pixel_data_image2 = image2.resize(resize, Image.NEAREST).convert('L')

        else:
            self.save_image(image2)

            if crop is None:
                pixel_data_image2 = list(self.buffer[image2][0].resize(resize, Image.NEAREST).convert('L').getdata())
            else:
                pixel_data_image2 = self.save_modified_image(image2, crop, resize)

        if bw_threshold is None:
            avg_pixel = sum(pixel_data_image1) / len(pixel_data_image1)
        else:
            # image1.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data_image1)
        image1_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

        if bw_threshold is None:
            avg_pixel = sum(pixel_data_image2) / len(pixel_data_image2)
        else:
            # image2.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data_image2)
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

        # image1.close()
        # image2.close()

        return fuzz.ratio(image1_hash, image2_hash)
