from Among_Us import execute_action


def count_x(image, y):
    return round(((y - (image.size[1] // 2)) / 42.5) ** 2 + 70)


def run(image):
    crop = (1145, 114, 1383, 961)

    image = image.crop(crop).convert('L')

    up_pos, down_pos = float("-inf"), float("inf")

    for y in range(image.size[1]):
        x = count_x(image, y)

        if 62 <= image.getpixel((x, y)) <= 70:
            up_pos = max(up_pos, y)
            down_pos = min(down_pos, y)

    center_pos = (down_pos + up_pos) // 2

    execute_action("mouse_move", crop[0] + count_x(image, center_pos), crop[1] + center_pos)
    execute_action("mouse_press")
    execute_action("mouse_move", crop[0] + count_x(image, image.size[1] // 2), crop[1] + image.size[1] // 2, 0)
    execute_action("mouse_release")
    execute_action("wait", 1)

    return True
