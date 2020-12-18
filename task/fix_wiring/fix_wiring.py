from Among_Us import execute_action

def run(screenshot, task_data, trigger):

    left_wires_pos = [
        (59, 182),
        (59, 370),
        (59, 555),
        (59, 741)
    ]

    right_wires_pos = [
        (834, 182),
        (834, 370),
        (834, 555),
        (834, 741)
    ]

    left_wires = [
        [c >= 126 for c in screenshot.getpixel((trigger[1][0] + pos[0], trigger[1][1] + pos[1]))]
        for pos in left_wires_pos
    ]
    right_wires = [
        [c >= 126 for c in screenshot.getpixel((trigger[1][0] + pos[0], trigger[1][1] + pos[1]))]
        for pos in right_wires_pos
    ]

    wire_map = [None] * len(left_wires)
    for i, left_wire in enumerate(left_wires):
        for j, right_wire in enumerate(right_wires):
            if left_wire == right_wire:
                wire_map[i] = j
                break

    if None in wire_map:
        return False

    for i, j in enumerate(wire_map):
        execute_action("mouse_move", trigger[1][0] + left_wires_pos[i][0], trigger[1][1] + left_wires_pos[i][1])
        execute_action("mouse_press")
        execute_action("mouse_move", trigger[1][0] + right_wires_pos[j][0], trigger[1][1] + right_wires_pos[j][1], 0.1)
        execute_action("mouse_release")

    execute_action("wait", 1)

    return True
