from tabulate import tabulate
import pandas as pd

data_res = []
x = [1, 2, 3, 4, 5, 6]
y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
data_res.append(x)
data_res.append(y)

def find_one_side_dif(x, y):
    diff = []
    for i in range(len(x) - 1):
        delta_x = x[i + 1] - x[i]
        delta_y = y[i + 1] - y[i]
        one_side_dif = round(delta_y / delta_x, 3)
        diff.append(one_side_dif)
    delta_x_last = x[-1] - x[-2]
    delta_y_last = y[-1] - y[-2]
    diff.append(round(delta_y_last / delta_x_last, 3))
    return diff


def find_second_side_dif(x, y):
    diff = []
    diff.append(round((y[2] - 2 * y[1] + y[0]) / ((x[2] - x[1]) * (x[1] - x[0])), 3))
    for i in range(1, len(x) - 1):
        delta_x = (x[i + 1] - x[i]) * (x[i] - x[i - 1])
        delta_y = y[i + 1] - 2 * y[i] + y[i - 1]
        second_side_dif = round(delta_y / delta_x, 3)
        diff.append(second_side_dif)
    delta_x_last = (x[-3] - x[-2]) * (x[-2] - x[-1])
    delta_y_last = y[-3] - 2 * y[-2] + y[-1]
    diff.append(round(delta_y_last / delta_x_last, 3))
    return diff


def find_dif_num(x, y):
    diff = []
    for i in range(len(x) - 1):
        tmp = (y[i] / x[i]) * (x[i + 1] / y[i + 1]) * ((y[i] - y[i + 1]) / (x[i] - x[i + 1]))
        diff.append( round(tmp, 3))
    tmp = (y[-2] / x[-2]) * (x[-1] / y[-1]) * ((y[-2] - y[-1]) / (x[-2] - x[-1]))
    diff.append(round(tmp, 3))
    return diff


def find_central_side_dif(x, y):
    diff = []
    diff.append(round((-3 * y[0] + 4 * y[1] - y[2]) / (x[2] - x[0]), 3))
    for i in range(1, len(x) - 1):
        delta_x = x[i + 1] - x[i - 1]
        delta_y = y[i + 1] - y[i - 1]
        central_side_dif = round(delta_y / delta_x, 3)
        diff.append(central_side_dif)
    delta_x_last = x[-1] - x[-2]
    delta_y_last = y[-1] - y[-2]
    diff.append(round(delta_y_last / delta_x_last, 3))
    return diff

def find_runge(x, y):
    diff = []
    for i in range(len(x) - 2):
        tmp = (-3 * y[i] + 4 * y[i + 1] - y[i + 2]) / (x[i + 2] - x[i])
        diff.append( round(tmp, 3))
    for i in range(len(x) - 2, len(x)):
        tmp = (3 * y[i] - 4 * y[i - 1] + y[i - 2]) / (-x[i - 2] + x[i])
        diff.append( round(tmp, 3))
    return diff

def find_runge_central(x, y):
    diff = []
    n = len(x)
    diff.append(0)
    diff.append(0)
    for i in range(2, n - 2):
        h = x[i + 1] - x[i - 1]
        h2 = x[i + 2] - x[i - 2]
        tmp = (y[i + 1] - y[i - 1]) / h  + ((y[i + 1] - y[i - 1]) / h - (y[i + 2] - y[i - 2]) / h2) / 3
        diff.append(round(tmp, 3))
    diff.append(0)
    diff.append(0)
    # h_forward = x[1] - x[0]
    # tmp_forward = (y[1] - y[0]) / h_forward
    # diff.insert(0, round(tmp_forward, 3))

    # h_backward = x[-1] - x[-2]
    # tmp_backward = (y[-1] - y[-2]) / h_backward
    # diff.append(round(tmp_backward, 3))

    return diff

# one_side = find_one_side_dif(x, y)
# data_res.append(one_side)

# central_side = find_central_side_dif(x, y)
# data_res.append(central_side)

# Runge_num = find_runge_central(x, y)
# data_res.append(Runge_num)

# dif_num = find_dif_num(x, y)
# data_res.append(dif_num)

# second_side = find_second_side_dif(x, y)
# data_res.append(second_side)

one_side = find_one_side_dif(x, y)
central_side = find_central_side_dif(x, y)
runge_num = find_runge_central(x, y)
dif_num = find_dif_num(x, y)
second_side = find_second_side_dif(x, y)

data = {
    'x': x,
    'y': y,
    'one_side': one_side,
    'central_side': central_side,
    'runge': runge_num,
    'align': dif_num,
    'second_side': second_side
}

df = pd.DataFrame(data)

print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))