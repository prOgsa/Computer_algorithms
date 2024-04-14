import math
import tabulate as tab
import matplotlib.pyplot as plt
import numpy as np
import copy

N = 2
n = 4
STEP_X = 0.1
X_BEG, X_END = 0, 4.2
X = 3.1
def read_from_file_to_list(name_file):
    data = []
    with open(name_file, 'r') as f:
        for line in f:
            elem = line.split()
            elem = [float(e) for e in elem]
            data.append(elem)
    return sorted(data)

data = read_from_file_to_list("data/data1.txt")

def find_points(x, n, x_data, y_data):
    ind = 0
    for i in range(len(x_data)):
        tmp = x_data[i] - x
        if (tmp > 0):
            ind = i
            break
    min_i = ind
    max_i = ind
    i = 0
    while i < n:
        if min_i > 0:
            min_i -= 1
            i += 1
        if max_i < len(y_data):
            max_i += 1
            i += 1

    return min_i, max_i

def divided_difference(x_data, y_data, n):
    result = []
    result.append(y_data[0])
    k = 1
    while len(y_data) != 1:
        data = []
        for i in range(len(y_data) - 1):
            data.append((y_data[i] - y_data[i + 1]) / (x_data[i] - x_data[i + k]))
        k += 1
        result.append(data[0])
        y_data = data
    return result

def p_func_n(x, data, n):
    x_data = [row[0] for row in data]
    y_data = [row[1] for row in data]

    min_i, max_i = find_points(x, n + 1, x_data, y_data)

    x_data = x_data[min_i:max_i + 1]
    y_data = y_data[min_i:max_i + 1]
    result = divided_difference(x_data, y_data, n)
    y = 0
    for i in range(n + 1):
        tmp = 1
        for j in range(i):
            tmp *= (x - x_data[j])
        y += result[i] * tmp
    return y

def make_new_table(data, n, x):
    x_data = [row[0] for row in data]
    y_data = [row[1] for row in data]
    min_i, max_i = find_points(x, n, x_data, y_data)
    data = data[min_i:max_i + 1]
    data_new = []
    for i in range(n):
        for j in range(len(data[i]) - 1):
            data_new.append([i, data[i]])
    return data_new

def divided_difference_hermit(data, n):
    result = []
    k = 1
    x_data = [row[1][0] for row in data]
    y_data = [row[1][1] for row in data]
    y1_data = [row[1][2] for row in data]
    y2_data = [row[1][3] for row in data]
    result.append(y_data[0])
    while len(y_data) != 1:
        data_new = []
        for i in range(len(y_data) - 1):
            if (data[i][0] == data[i + k][0] and k == 1):
                data_new.append(y1_data[i])
            elif (data[i][0] == data[i + k][0] and k == 2):
                data_new.append(y2_data[i] / 2)
            elif data[i][0] != data[i + k][0]:
                data_new.append((y_data[i] - y_data[i + 1]) / (x_data[i] - x_data[i + k]))
        k += 1
        result.append(data_new[0])
        y_data = data_new
    return result

def p_func_e(x, data, n):
    data_new = make_new_table(data, n, x)
    result = divided_difference_hermit(data_new, n)
    x_data = [row[1][0] for row in data_new]
    y = 0
    for i in range(len(result)):
        tmp = 1
        for j in range(i):
            tmp *= (x - x_data[j])
        y += result[i] * tmp
    return y

def binary_search(func, left, right, eps=0.00001):
    while right - left > eps:
        mid = (left + right) / 2
        if func(left) * func(mid) < 0:
            right = mid
        else:
            left = mid
    return (left + right) / 2


def output(data, n, x):
    print("x = ", x)
    new_data = copy.deepcopy(data)
    tmp = copy.deepcopy(data)
    data1 = read_from_file_to_list("data/data2.txt")
    data2 = read_from_file_to_list("data/data3.txt")
    table = [
        [1, round(p_func_n(x, data, 1), 4), round(p_func_e(x, data, 1), 4)],
        [2, round(p_func_n(x, data, 2), 4), round(p_func_e(x, data, 2), 4)],
        [3, round(p_func_n(x, data, 3), 4), round(p_func_e(x, data, 3), 4)],
        [4, round(p_func_n(x, data, 4), 4), round(p_func_e(x, data, 4), 4)],
        [5, round(p_func_n(x, data, 5), 4), round(p_func_e(x, data, 5), 4)]
    ]
    table_1 = tab.tabulate(table, headers=["n", "полином Ньютона", "полином Эрмита"], tablefmt="pretty")
    draw_graphic(data, n)
    print(table_1)
    print("Корень табличной функции найденный с помощью обратной интерполяции полинома Ньютона при n = {}:".format(n + 1), f"{binary_search(lambda x: p_func_n(x, data, n), 0, 10):.4f}")
    print("Корень табличной функции найденный с помощью обратной интерполяции полинома Эрмита при n = {}:".format(n), f"{binary_search(lambda x: p_func_e(x, data, n), 0, 10):.4f}")
    print()
    data_new = create_one_data_from_two(data1, data2, 2)
    x = find_root_n(data_new, 3, 0)
    print("Корень системы уравнений (x, y): ", x, p_func_n(x, data1, 3))

def find_root_n(data, n, x):
    for row in data:
        tmp = row[0]
        row[0] = row[1]
        row[1] = tmp
    return p_func_n(x, data, n)

def get_reverse_table(mat):
    rev = []
    for row in mat:
        now = []
        now.extend((row[1], row[0]))
        if (len(row) >= 3):
            now.append(1 / row[2])
        if (len(row) >= 4):
            now.append(row[3] / row[2] ** 3)
        rev.append(now)
    return rev

def find_root_hermite(data, n, x):
    original_data = get_reverse_table(data)
    return p_func_e(x, original_data, n)

def draw_graphic(data, n):
    newton_data, hermit_data = list(), list()

    x_coord = np.arange(X_BEG, X_END, STEP_X)
    for x in x_coord:
        i = 0
        while x < data[i][0]:
            i += 1
        if x == data[i][0]:
            y = data[i][1]
            newton_data.append([x, y])
            hermit_data.append([x, y])
        else:
            x_data = [row[0] for row in data]
            y_data = [row[1] for row in data]
            min_i, max_i = find_points(x, n + 1, x_data, y_data)
            data[min_i:max_i + 1]

            p = p_func_n(x, data, n)
            h = p_func_e(x, data, n)

            newton_data.append([x, p])
            hermit_data.append([x, h])

    # Таблица
    # tab = PrettyTable()
    # tab.field_names = ['x', 'Newton', 'Hermit', 'diff']
    # for i in range(len(newton_data)):
    #     tab.add_row([f'{newton_data[i][0]:.{accuracy}f}',
    #                  f'{newton_data[i][1]:.{accuracy}f}', f'{hermit_data[i][1]:.{accuracy}f}',
    #                  f'{newton_data[i][1] - hermit_data[i][1]:.{accuracy}f}'])
    # print(f'n = {n}')
    # print(tab)

    y_values_newton = list(map(lambda xy: xy[1], newton_data))
    y_values_hermite = list(map(lambda xy: xy[1], hermit_data))

    plt.plot(x_coord, y_values_newton, color='r', label='Newton')
    plt.plot(x_coord, y_values_hermite, color='b', label='Hermit')

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polynomials Newton and Hermite')

    plt.legend()
    plt.show()


def create_one_data_from_two(data1, data2, n):
    data_new = []
    for row in data1:
        data_new.append([row[0], p_func_n(row[0], data2, n) - row[1]])
    
    for row in data2:
        data_new.append([row[0], row[1] - p_func_n(row[0], data1, n)])
    
    return sorted(data_new)
output(data, n, X)

def find_points_of_derivative_zero(x_data, y_data):
    points_of_derivative_zero = []
    for i in range(1, len(x_data) - 1):
        if derivative_at_point(x_data, y_data, i) == 0:
            points_of_derivative_zero.append(i)
    return points_of_derivative_zero

def make_new_table_with_derivative_zero(data, n, x):
    x_data = [row[0] for row in data]
    y_data = [row[1] for row in data]
    min_i, max_i = find_points(x, n, x_data, y_data)
    data = data[min_i:max_i + 1]
    points_of_derivative_zero = find_points_of_derivative_zero(x_data, y_data)
    for point in points_of_derivative_zero:
        data.append([x_data[point], y_data[point]])
    return sorted(data)

def divided_difference_hermit(data, n):
    result = []
    k = 1
    x_data = [row[1][0] for row in data]
    y_data = [row[1][1] for row in data]
    y1_data = [row[1][2] for row in data]
    y2_data = [row[1][3] for row in data]
    result.append(y_data[0])
    while len(y_data) != 1:
        data_new = []
        for i in range(len(y_data) - 1):
            if (data[i][0] == data[i + k][0] and k == 1):
                data_new.append(y1_data[i])
            elif (data[i][0] == data[i + k][0] and k == 2):
                data_new.append(y2_data[i] / 2)
            elif data[i][0] != data[i + k][0]:
                data_new.append((y_data[i] - y_data[i + 1]) / (x_data[i] - x_data[i + k]))
        k += 1
        result.append(data_new[0])
        y_data = data_new
    return result



# x = float(input("Введите фиксированный x: "))
# if x < data[0][0] or x > data[len(data) - 1][0]:
#     print("Числа нет в таблице")
# else:

# n = int(input("Введите степень n для аппроксимирующего полинома Ньютона: "))
# if n < 0:
#     print("Степень n меньше нуля")
# elif n > 5:
#     print("Степень больше 5, результат не точен")
# else:
# s = int(input("Введите количество узлов для аппроксимирующего полинома Эрмита:"))
# if s < 0:
#     print("Степень n меньше нуля")
# elif s > 5:
#     print("Степень больше 5, результат не точен")
# else:
