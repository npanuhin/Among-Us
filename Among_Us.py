import pyautogui
# import win32gui
# from win32api import GetSystemMetrics
# import win32con
# import win32ui

from time import sleep
from PIL import ImageGrab
from json import load as json_load
import importlib
import sys
import os

from compare import ImageCompare

INITIAL_TRIGGER_THRESHOLD = 90

imageCompare = ImageCompare()


TASK_TYPES = ("task", "sabotage")


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

    for task_type in TASK_TYPES:
        for task_name in os.listdir(task_type):
            with open(mkpath(task_type, task_name, "data.json"), 'r', encoding="utf-8") as file:
                task_data = json_load(file, encoding="utf-8")

            assert "triggers" in task_data and isinstance(task_data["triggers"], list), "Error in {}/{}".format(task_type, task_name)
            assert "actions" in task_data and isinstance(task_data["triggers"], list), "Error in {}/{}".format(task_type, task_name)

            if isinstance(task_data["actions"], str):
                sys.path.append(mkpath(task_type, task_name))
                try:
                    task_data["actions"] = importlib.import_module(task_name)
                except Exception:
                    raise ImportError(task_name)

            for trigger in task_data["triggers"]:
                assert isinstance(trigger, list) and (
                    len(trigger) == 2 or
                    (len(trigger) == 3 and isinstance(trigger[2], int))
                ) and \
                    isinstance(trigger[0], str) and isinstance(trigger[1], list) and \
                    len(trigger[1]) == 4 and (isinstance(trigger[1][i], int) for i in range(4)), \
                    "Error in {}/{}: {}".format(task_type, task_name, trigger)

                trigger[0] = mkpath(task_type, task_name, trigger[0])

            tasks[task_name] = task_data

    for task_name, task_data in tasks.items():
        print("{}:\n{}".format(task_name, task_data))

    print("Starting...")

    # exit()

    iteration_count = 0

    while True:
        screenshot = take_screenshot()

        best_action, best_comparison, best_trigger = None, float("-inf"), None

        for task_name, task_data in tasks.items():
            for trigger in task_data["triggers"]:

                comparison = imageCompare.compare(screenshot, trigger[0], trigger[1])

                if comparison >= (trigger[2] if len(trigger) == 3 else INITIAL_TRIGGER_THRESHOLD) and \
                        comparison > best_comparison:
                    best_comparison = comparison
                    best_action = task_name
                    best_trigger = trigger

        if best_action is not None:
            print("Triggered task \"{}\"".format(best_action))

            execute_action("wait", 0.1)

            actions = tasks[best_action]["actions"]

            if isinstance(actions, list):
                for action in actions:
                    execute_action(action[0], *action[1:])
            else:
                if not actions.run(screenshot, tasks[best_action], best_trigger):
                    print("Task \"{}\" failed!".format(best_action))
                    execute_action("wait", 1)

        del screenshot

        print("Iteration #{}".format(iteration_count))
        iteration_count += 1


if __name__ == "__main__":
    main()

    # sleep(3)
    # take_screenshot().save(["reference.png")]

    # print("Compare:", compare("tasks/swipe_card/reference.png", take_screenshot(), [512, 92, 1407, 968]))
