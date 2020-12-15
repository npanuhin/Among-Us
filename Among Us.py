import pyautogui
import win32gui
from win32api import GetSystemMetrics
import win32con
import win32ui

from time import sleep
from PIL import Image
# from traceback import format_exc
from json import load as json_load
import os

COMPARE_THRESHOLD = 100


def mkpath(*paths):
    return os.path.normpath(os.path.join(*paths))


def take_screenshot(path="screen.png"):
    hwnd = win32gui.GetDesktopWindow()
    width = GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    x = GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    y = GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (x, y), win32con.SRCCOPY)

    # saveBitMap.SaveBitmapFile(saveDC, 'screenshot.bmp')

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    image = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    return image


def compare(image1, image2, crop):
    # image1 = Image.open(file1)
    # image2 = Image.open(file2)

    size = [30, 30]

    image1 = image1.crop(crop).resize(size, Image.NEAREST).convert('L')
    image2 = image2.crop(crop).resize(size, Image.NEAREST).convert('L')

    pixel_data = list(image1.getdata())
    avg_pixel = sum(pixel_data) / len(pixel_data)
    bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data)
    image1_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

    pixel_data = list(image2.getdata())
    avg_pixel = sum(pixel_data) / len(pixel_data)
    bits = "".join(str(int(px >= avg_pixel)) for px in pixel_data)
    image2_hash = str(hex(int(bits, 2)))[2:][::-1].upper()

    # image1.show()
    # image2.show()

    # print(image1_hash)
    # print()
    # print(image2_hash)

    if len(image1_hash) >= len(image2_hash):
        result = min(
            sum(abs(ord(image1_hash[start + i]) - ord(image2_hash[i])) for i in range(len(image2_hash)))
            for start in range(len(image1_hash) - len(image2_hash) + 1)
        )
    else:
        result = min(
            sum(abs(ord(image1_hash[i]) - ord(image2_hash[start + i])) for i in range(len(image1_hash)))
            for start in range(len(image2_hash) - len(image1_hash) + 1)
        )

    # image1.show()
    # image1.save("result.png")

    image1.close()
    image2.close()

    return result


def execute_actions(actions):
    for action, args in actions:

        if action == "sleep":
            sleep(args[0])

        elif action == "mouse_move":
            pyautogui.moveTo(args[0], args[1], 0 if len(args) < 3 else args[2])

        elif action == "mouse_press":
            pyautogui.mouseDown()

        elif action == "mouse_release":
            pyautogui.mouseUp()

        elif action == "mouse_click":
            pyautogui.click()

        elif action == "mouse_doubleclick":
            pyautogui.doubleClick()

        elif action == "press_key":
            pyautogui.press(args[0])


def main():
    tasks = {}

    for task_name in os.listdir("tasks"):
        with open(mkpath("tasks", task_name, "data.json"), 'r', encoding="utf-8") as file:
            task_data = json_load(file, encoding="utf-8")

        task_data["trigger"] = mkpath("tasks", task_name, task_data["trigger"])
        task_data["actions"] = [(action[0], action[1:]) for action in task_data["actions"]]

        tasks[task_name] = task_data

    print("Starting...")

    while True:
        image = take_screenshot()

        best_task, best_comparison = None, float("inf")

        for task_name in tasks:
            task_data = tasks[task_name]

            comparison = compare(image, Image.open(task_data["trigger"]), task_data["crop"])

            if comparison < best_comparison:
                best_comparison = comparison
                best_task = task_name

        if best_comparison <= COMPARE_THRESHOLD:
            print("Triggered task \"{}\"".format(best_task))

            task_data = tasks[best_task]

            execute_actions(task_data["actions"])

        print("Iteration")


if __name__ == "__main__":
    main()
    # sleep(3)
    # take_screenshot().save("screen.png")
    # print("Compare:", compare("reference.png", "screen.png"))
