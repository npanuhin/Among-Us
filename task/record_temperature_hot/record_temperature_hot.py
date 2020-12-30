from Among_Us import mkpath, execute_action, imageCompare, take_screenshot, INITIAL_TRIGGER_THRESHOLD


def run(screenshot, task_data, trigger):
    execute_action("mouse_move", 635, 341)
    execute_action("mouse_press")

    while imageCompare(take_screenshot(), mkpath("task", "record_temperature_hot", "reference.png"), crop=trigger[1]) >= \
            (trigger[2] if len(trigger) == 3 else INITIAL_TRIGGER_THRESHOLD):
        execute_action("wait", 0.1)

    execute_action("mouse_release")

    execute_action("wait", 1)

    return True
