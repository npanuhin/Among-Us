from Among_Us import mkpath, imageCompare, execute_action  # , IMAGE_RESIZE_FUNC
import os

top_row_y = 398
bottom_row_y = 552
left_to_right = (589, 1202, 153)

cell_size = (130, 130)

def run(screenshot, task_data, trigger):

    numbers = list(screenshot.crop((x, top_row_y, x + cell_size[0], top_row_y + cell_size[1])) for x in range(*left_to_right)) + \
        list(screenshot.crop((x, bottom_row_y, x + cell_size[0], bottom_row_y + cell_size[1])) for x in range(*left_to_right))

    order = [None] * 10

    for i, image in enumerate(numbers):
        # image = image.resize((32, 32), IMAGE_RESIZE_FUNC).convert('1')
        # image.save(mkpath("task", "unlock_manifolds", "numbers", str(i) + "_.png"))

        best_number, best_comparison = None, float("-inf")

        for filename in os.listdir(mkpath("task", "unlock_manifolds", "numbers")):
            number = int(os.path.splitext(filename)[0])

            comparison = imageCompare(
                image,
                mkpath("task", "unlock_manifolds", "numbers", filename),
                resize=(32, 32),
                bw_threshold=80
            )

            if comparison > best_comparison:
                best_comparison = comparison
                best_number = number

        order[best_number - 1] = i

    print("Orger:", " ".join(map(str, order)))

    if None in order:
        return False

    for pos in order:
        if pos < 5:
            execute_action("mouse_move", 589 + 153 * (pos % 5) + cell_size[0] // 2, 398 + cell_size[1] // 2)
        else:
            execute_action("mouse_move", 589 + 153 * (pos % 5) + cell_size[0] // 2, 552 + cell_size[1] // 2)
        execute_action("mouse_click")
        # execute_action("wait", 0.5)

    execute_action("wait", 1)

    return True
