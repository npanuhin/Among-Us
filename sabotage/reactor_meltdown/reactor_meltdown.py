from Among_Us import mkpath, execute_action, take_screenshot, imageCompare, INITIAL_TRIGGER_THRESHOLD

def run(screenshot, task_data, trigger):

    hand_press = (973, 712)

    execute_action("mouse_move", *hand_press)
    execute_action("mouse_press")

    while True:
        if imageCompare.compare(
            take_screenshot(),
            mkpath("sabotage", "reactor_meltdown", "reference.png"), crop=trigger[2]
        ) < (trigger[3] if len(trigger) == 3 else INITIAL_TRIGGER_THRESHOLD):
            break
        execute_action("wait", 0.5)

    execute_action("mouse_release")
    execute_action("wait", 1)
    return True
