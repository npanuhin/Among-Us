from Among_Us import mkpath, take_screenshot, imageCompare, execute_action


def run(screenshot):
    compare_box = [970, 204, 1558, 875]

    left_box = (482, 424, 830, 772)
    right_box = (1086, 424)

    cell_distance = ((left_box[2] - left_box[0]) // 3, (left_box[3] - left_box[1]) // 3)

    count = 5

    order = []
    last_cell = None

    while True:
        screenshot = take_screenshot()
        if imageCompare.compare(screenshot, mkpath("tasks", "start_reactor", "waiting.png"), crop=compare_box) >= \
                imageCompare.compare(screenshot, mkpath("tasks", "start_reactor", "reference.png"), crop=compare_box) and order:
            # print(order)

            for x, y in order:
                execute_action("mouse_move", right_box[0] + x, right_box[1] + y)
                execute_action("mouse_click")
                # execute_action("wait", 0.3)

            order = []
            count -= 1

        else:
            cur_cell = None

            for i in range(left_box[0] + cell_distance[0] // 2, left_box[2], cell_distance[0]):
                for j in range(left_box[1] + cell_distance[1] // 2, left_box[3], cell_distance[1]):
                    if screenshot.getpixel((i, j))[2] >= 250:
                        cur_cell = (i - left_box[0], j - left_box[1])
                        break

            if last_cell is None and cur_cell is not None:
                order.append(cur_cell)

            last_cell = cur_cell

        if count <= 0:
            break

    execute_action("wait", 1)
