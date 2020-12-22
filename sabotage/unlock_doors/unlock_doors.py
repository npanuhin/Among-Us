from Among_Us import execute_action

left_column = 877
right_column = 1210
top_row = 220
bottom_row = 800


def run(screenshot, task_data, trigger):

    for y in range(4):
        y = top_row + (bottom_row - top_row) / 3 * y
        for x in range(2):
            x = left_column + (right_column - left_column) / 1 * x

            if (screenshot.getpixel((x, y))[0] >= 120):
                execute_action("mouse_move", x, y)
                execute_action("mouse_click")

    execute_action("wait", 1)

    return True
