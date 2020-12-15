from Among_Us import execute_action


def count_x(image, y):
    return round(((y - (image.size[1] // 2)) / 42.5) ** 2 + 70)


def run(screenshot):
    crop = (1145, 114, 1383, 961)

    screenshot = screenshot.crop(crop).convert('L')

    down_pos, up_pos = float('inf'), float("-inf")

    for y in range(screenshot.size[1]):
        x = count_x(screenshot, y)

        if 62 <= screenshot.getpixel((x, y)) <= 70:
            up_pos = max(up_pos, y)
            down_pos = min(down_pos, y)

    if down_pos == float("inf") or up_pos == float("-inf"):
        return False

    center_pos = (down_pos + up_pos) // 2

    execute_action("mouse_move", crop[0] + count_x(screenshot, center_pos), crop[1] + center_pos)
    execute_action("mouse_press")
    execute_action("mouse_move", crop[0] + count_x(screenshot, screenshot.size[1] // 2), crop[1] + screenshot.size[1] // 2, 0)
    execute_action("mouse_release")
    execute_action("wait", 1)

    return True
