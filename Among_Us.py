import pyautogui
# import win32gui
# from win32api import GetSystemMetrics
# import win32con
# import win32ui

from time import sleep
from PIL import ImageGrab
# from fuzzywuzzy import process
# from traceback import format_exc
from json import load as json_load
import importlib
import sys
import os


from compare import ImageCompare

INITIAL_COMPARE_THRESHOLD = 80

imageCompare = ImageCompare()


def mkpath(*paths):
    return os.path.normpath(os.path.join(*paths))


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

    for task_name in tasks:
        print("{}:\n{}".format(task_name, tasks[task_name]))

    print("Starting...")

    while True:
        screenshot = take_screenshot()

        best_task, best_comparison = None, float("-inf")

        for task_name in tasks:
            task_data = tasks[task_name]

            comparison = imageCompare.compare(screenshot, mkpath("tasks", task_name, task_data["trigger"]), task_data["crop"])

            if comparison > (task_data["trigger_threshold"] if "trigger_threshold" in task_data else INITIAL_COMPARE_THRESHOLD) and \
                    comparison > best_comparison:
                best_comparison = comparison
                best_task = task_name

        if best_task is not None:
            print("Triggered task \"{}\"".format(best_task))

            actions = tasks[best_task]["actions"]

            if isinstance(actions, list):
                for action in actions:
                    execute_action(action[0], *action[1:])
            else:
                if not actions.run(screenshot):
                    print("Task \"{}\" failed!".format(best_task))
                    execute_action("wait", 1)

        screenshot.close()

        # print("Iteration")


if __name__ == "__main__":
    main()

    # sleep(3)
    # take_screenshot().save("reference.png")

    # print("Compare:", compare("tasks/swipe_card/reference.png", take_screenshot(), [512, 92, 1407, 968]))
