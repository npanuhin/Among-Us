from Among_Us import mkpath, execute_action, take_screenshot, imageCompare, INITIAL_COMPARE_THRESHOLD

def run(screenshot, task_data):

    hand_press = (973, 712)

    execute_action("mouse_move", *hand_press)
    execute_action("mouse_press")

    while True:
        if imageCompare.compare(
            take_screenshot(),
            mkpath("tasks", "reactor_meltdown", "reference.png"), crop=task_data["trigger_region"]
        ) < INITIAL_COMPARE_THRESHOLD:
            break
        execute_action("wait", 0.5)

    execute_action("mouse_release")
    execute_action("wait", 1)
    return True
