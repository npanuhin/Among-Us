from Among_Us import execute_action


def run(screenshot, task_data, trigger):

    leavers_y = 786

    delta = 115

    left_pos, right_pos = float("inf"), float("-inf")

    for x in range(task_data["trigger_region"][0], task_data["trigger_region"][2] + 1):
        if screenshot.getpixel((x, leavers_y))[0] >= 250:
            left_pos = min(left_pos, x)
            right_pos = max(right_pos, x)

    if left_pos == float("inf") or right_pos == float("-inf"):
        return False

    center_x = (left_pos + right_pos) // 2

    execute_action("mouse_move", center_x, leavers_y)
    execute_action("mouse_press")
    execute_action("mouse_move", center_x, leavers_y - delta, 0)
    execute_action("mouse_release")

    execute_action("wait", 1)

    return True
