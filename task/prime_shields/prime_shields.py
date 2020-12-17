from Among_Us import execute_action, take_screenshot


def run(screenshot, task_data, trigger):
    shields_pos = [
        (730, 415),
        (960, 290),
        (1180, 415),
        (1180, 670),
        (960, 800),
        (730, 670),
        (960, 540)
    ]

    for x, y in shields_pos:
        cur_state = screenshot.getpixel((x, y))
        execute_action("mouse_move", x, y)
        execute_action("mouse_click")
        execute_action("wait", 0.1)
        screenshot = take_screenshot()
        alternative_state = screenshot.getpixel((x, y))

        if sum(cur_state) > sum(alternative_state):
            execute_action("mouse_click")

    execute_action("wait", 1)

    return True
