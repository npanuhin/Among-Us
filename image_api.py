from fuzzywuzzy import fuzz
from PIL import Image, ImageGrab

# import win32gui
# from win32api import GetSystemMetrics
# import win32con
# import win32ui


def take_screenshot(path="screen.png"):
    return ImageGrab.grab()

    # hwnd = win32gui.GetDesktopWindow()
    # width = GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    # height = GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    # x = GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    # y = GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    # hwndDC = win32gui.GetWindowDC(hwnd)
    # mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # saveDC = mfcDC.CreateCompatibleDC()

    # saveBitMap = win32ui.CreateBitmap()
    # saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # saveDC.SelectObject(saveBitMap)
    # saveDC.BitBlt((0, 0), (width, height), mfcDC, (x, y), win32con.SRCCOPY)

    # # saveBitMap.SaveBitmapFile(saveDC, 'screenshot.bmp')

    # bmpinfo = saveBitMap.GetInfo()
    # bmpstr = saveBitMap.GetBitmapBits(True)
    # image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    # mfcDC.DeleteDC()
    # saveDC.DeleteDC()
    # win32gui.ReleaseDC(hwnd, hwndDC)

    # return image


class ImageCompare:
    def __init__(self, IMAGE_RESIZE_FUNC):
        self.IMAGE_RESIZE_FUNC = IMAGE_RESIZE_FUNC
        self.buffer = {
            # [
            #     full_image,
            #     {
            #         hash(tuple(crop + resize)): {
            #             image.crop(crop).resize(resize, self.IMAGE_RESIZE_FUNC).convert('L')
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
                self.buffer[path][0].crop(crop).resize(resize, self.IMAGE_RESIZE_FUNC).convert('L').getdata()
            )

        return self.buffer[path][1][hash(tuple(crop + resize))]

    def get_pixel_image_data(self, image, crop, resize):
        if not isinstance(image, str):
            if crop is not None:
                image = image.crop(crop)
            pixel_image_data = list(image.resize(resize, self.IMAGE_RESIZE_FUNC).convert('L').getdata())

        else:
            self.save_image(image)

            if crop is None:
                pixel_image_data = list(self.buffer[image][0].resize(resize, self.IMAGE_RESIZE_FUNC).convert('L').getdata())
            else:
                pixel_image_data = self.save_modified_image(image, crop, resize)

        return pixel_image_data

    def compare(self, image1, image2, crop=None, resize=[16, 16], bw_threshold=None):
        pixel_image_data1 = self.get_pixel_image_data(image1, crop=crop, resize=resize)
        pixel_image_data2 = self.get_pixel_image_data(image2, crop=crop, resize=resize)

        if bw_threshold is None:
            avg_pixel = sum(pixel_image_data1) / len(pixel_image_data1)
        else:
            # image1.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_image_data1)
        image1_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

        if bw_threshold is None:
            avg_pixel = sum(pixel_image_data2) / len(pixel_image_data2)
        else:
            # image2.show()
            avg_pixel = bw_threshold

        bits = "".join(str(int(px >= avg_pixel)) for px in pixel_image_data2)
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
