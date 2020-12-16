from Among_Us import mkpath, execute_action, imageCompare, take_screenshot


def run(screenshot, task_data):
    execute_action("mouse_move", 635, 341)
    execute_action("mouse_press")

    while imageCompare.compare(take_screenshot(), mkpath("task", "record_temperature_hot", "reference.png")):
        execute_action("wait", 0.2)

    execute_action("mouse_release")

    return True
