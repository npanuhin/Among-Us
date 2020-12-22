import pyautogui

from time import sleep
from PIL.Image import NEAREST
from json import load as json_load
import importlib
import sys
import os

IMAGE_RESIZE_FUNC = NEAREST

INITIAL_TRIGGER_THRESHOLD = 90

TASK_TYPES = ("task", "sabotage")

from image_api import ImageCompare, take_screenshot

imageCompare = ImageCompare(IMAGE_RESIZE_FUNC).compare


def mkpath(*paths):
    return os.path.normpath(os.path.join(*paths))


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
    print("Starting...")

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
        print("{}: {}".format(task_name, task_data))

    print("Compiling images...")

    # exit()

    # iteration_count = 0
    compiled = False
    logged_compiled = False

    while True:
        if not logged_compiled and compiled:
            logged_compiled = True
            print("Watching...")

        screenshot = take_screenshot()

        best_action, best_comparison, best_trigger = None, float("-inf"), None

        for task_name, task_data in tasks.items():
            for trigger in task_data["triggers"]:

                comparison = imageCompare(screenshot, trigger[0], trigger[1])

                if comparison >= (trigger[2] if len(trigger) == 3 else INITIAL_TRIGGER_THRESHOLD) and \
                        comparison > best_comparison:
                    best_comparison = comparison
                    best_action = task_name
                    best_trigger = trigger

        if best_action is not None:
            print("Triggered task \"{}\"".format(best_action))

            # execute_action("wait", 0.15)

            actions = tasks[best_action]["actions"]

            if isinstance(actions, list):
                for action in actions:
                    execute_action(action[0], *action[1:])
            else:
                if not actions.run(screenshot, tasks[best_action], best_trigger):
                    print("Task \"{}\" failed!".format(best_action))
                    execute_action("wait", 1)

            print("Watching...")

        screenshot.close()

        # print("Iteration #{}".format(iteration_count))
        # iteration_count += 1
        compiled = True


if __name__ == "__main__":
    main()

    # sleep(3)
    # take_screenshot().save("reference.png")

    # print("Compare:", compare("tasks/swipe_card/reference.png", take_screenshot(), [512, 92, 1407, 968]))
