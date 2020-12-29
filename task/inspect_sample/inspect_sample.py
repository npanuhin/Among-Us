from Among_Us import execute_action, take_screenshot

buttons = [
    (733, 847),
    (846, 847),
    (960, 847),
    (1073, 847),
    (1186, 847)
]

tubes_y = 594

start_button = (1260, 935)

def run(screenshot, task_data, trigger):

    while True:
        screenshot = take_screenshot()
        if screenshot.getpixel(start_button)[0] < 100 and \
                screenshot.getpixel(start_button)[1] >= 120 and \
                screenshot.getpixel(start_button)[2] < 100:
            execute_action("mouse_move", *start_button)
            execute_action("mouse_click")
            execute_action("wait", 0.2)
            execute_action("key_press", "esc")
            break

        for button in buttons:
            if screenshot.getpixel((button[0], tubes_y))[0] >= 200 and \
                    screenshot.getpixel((button[0], tubes_y))[1] < 180 and \
                    screenshot.getpixel((button[0], tubes_y))[2] < 180:
                execute_action("mouse_move", *button)
                execute_action("mouse_click")
                break
            else:
                continue
            break

        execute_action("wait", 0.1)

    execute_action("wait", 1)

    return True
