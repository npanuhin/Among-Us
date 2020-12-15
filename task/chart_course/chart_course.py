from Among_Us import execute_action


def run(screenshot, task_data):

    pixel_threshold = (70, 100)

    top, bottom = 265, 814

    stars_x_pos = (566, 763, 959, 1157, 1353)

    screenshot = screenshot.convert('L')

    last_center_pos = None

    for step, x in enumerate(stars_x_pos):

        down_pos, up_pos = float('inf'), float("-inf")

        for y in range(top, bottom + 1):
            if pixel_threshold[0] <= screenshot.getpixel((x, y)) <= pixel_threshold[1]:
                down_pos = min(down_pos, y)
                up_pos = max(up_pos, y)

        # print(x, down_pos, up_pos)

        if down_pos == float("inf") or up_pos == float("-inf"):
            return False

        center_pos = (down_pos + up_pos) // 2

        mouse_y = center_pos + 30 * (0 if last_center_pos is None else 1 if last_center_pos <= center_pos else -1)

        last_center_pos = center_pos

        if step == 0:
            execute_action("mouse_move", x, mouse_y)
            execute_action("mouse_press")

        elif step == len(stars_x_pos) - 1:
            execute_action("mouse_move", x + 30, mouse_y, 0.5)
            execute_action("wait", 0.3)
            execute_action("mouse_release")

        else:
            execute_action("mouse_move", x + 30, mouse_y, 0.5)
            execute_action("wait", 0.3)

    execute_action("wait", 1)

    return True
