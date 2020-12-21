from Among_Us import execute_action, take_screenshot


def run(screenshot, task_data, trigger):

    labels = [
        (1235, 230, 1235, 310),
        (1235, 500, 1235, 580),
        (1235, 770, 1235, 835)
    ]

    for x, y, click_x, click_y in labels:
        execute_action("mouse_move", click_x, click_y)
        while True:
            screenshot = take_screenshot()
            if sum(screenshot.getpixel((x, y))) >= 250:
                execute_action("mouse_click")
                break

    execute_action("wait", 1)
    return True
