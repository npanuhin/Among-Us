from Among_Us import execute_action

x_positions = (613, 790, 963, 1138, 1312)

indicators = [(x, 900) for x in x_positions]

switches = [(x, 784) for x in x_positions]

def run(screenshot, task_data, trigger):

    for i in range(len(x_positions)):
        if screenshot.getpixel(indicators[i])[1] <= 150:
            execute_action("mouse_move", *switches[i])
            execute_action("mouse_click")

    execute_action("wait", 1)
    return True
