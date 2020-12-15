import pyautogui
import win32gui
from win32api import GetSystemMetrics
import win32con
import win32ui

from time import sleep
from PIL import Image
from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
# from traceback import format_exc
from json import load as json_load
import importlib
import sys
import os

COMPARE_THRESHOLD = 80


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

    mfcDC.DeleteDC()
    saveDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    return image


def compare(image1, image2, crop=None, resize=(8, 8), bw_threshold=None):
    # image1 = Image.open(file1)
    # image2 = Image.open(file2)

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


def execute_action(action, *args):
    print("Executing", action, args)

    if action == "wait":
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

        if isinstance(task_data["actions"], str):
            sys.path.append(mkpath("tasks", task_name))
            task_data["actions"] = importlib.import_module(task_name)

        tasks[task_name] = task_data

    print(tasks)

    print("Starting...")

    while True:
        image = take_screenshot()

        best_task, best_comparison = None, float("-inf")

        for task_name in tasks:
            task_data = tasks[task_name]

            comparison = compare(image, Image.open(mkpath("tasks", task_name, task_data["trigger"])), task_data["crop"])

            if comparison > best_comparison:
                best_comparison = comparison
                best_task = task_name

        if best_comparison >= COMPARE_THRESHOLD:
            print("Triggered task \"{}\"".format(best_task))

            actions = tasks[best_task]["actions"]

            if isinstance(actions, list):
                for action in actions:
                    execute_action(action[0], *action[1:])
            else:
                if not actions.run(image):
                    print("Task \"{}\" failed!".format(task_name))

        image.close()

        print("Iteration")


if __name__ == "__main__":
    main()
    # sleep(3)
    # take_screenshot().save("reference.png")
    # print("Compare:", compare(Image.open("tasks/swipe_card/reference.png"), take_screenshot(), [512, 92, 1407, 968]))
