from Among_Us import mkpath, execute_action, take_screenshot, imageCompare, INITIAL_COMPARE_THRESHOLD

def run(screenshot):

    box = [514, 95, 1406, 986]

    hand_press = (973, 712)

    execute_action("mouse_move", *hand_press)
    execute_action("mouse_press")

    while True:
        if not imageCompare.compare(take_screenshot(), mkpath("tasks", "reactor_meltdown", "reference.png"), crop=box) >= INITIAL_COMPARE_THRESHOLD:
            break
        execute_action("wait", 0.5)

    execute_action("mouse_release")
    execute_action("wait", 1)
    return True
