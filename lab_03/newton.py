def find_points(x, n, x_data, y_data):
    ind = 0
    while ind < len(x_data) and x > x_data[ind]:
        ind += 1
    ind -= 1 if ind != 0 else 0

    left = ind
    right = ind
    for i in range(n - 1):
        if i % 2 == 0:
            if left == 0:
                right += 1
            else:
                left -= 1
        else:
            if right == len(x_data) - 1:
                left -= 1
            else:
                right += 1
    return left, right + 1
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

def newton(x, data, n):
    x_data = [row[0] for row in data]
    y_data = [row[1] for row in data]

    min_i, max_i = find_points(x, n + 1, x_data, y_data)

    x_data = x_data[min_i:max_i]
    y_data = y_data[min_i:max_i]
    result = divided_difference(x_data, y_data, n)

    y = 0
    for i in range(n + 1):
        tmp = 1
        for j in range(i):
            tmp *= (x - x_data[j])
        y += result[i] * tmp
    return y

def find_3d_newton(data, x, y, nx, ny):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, newton(x, temp, nx)])
    return newton(y, temp_table, ny)

def find_4d_newton(data, x, y, z, nx, ny, nz):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_3d_newton(line[1], x, y, nx, ny))
        i += 1
    return newton(z, temp, nz)

def find_3d_newton1(data, x_list, y_list,  x, y, nx, ny):
    temp_table = []
    tmp = data
    for j in range(data.shape[0]):
        temp = []
        for k in range(data.shape[1]):
            temp.append([x_list[k], tmp[j][k]])
        temp_table.append([y_list[j],  newton(x, temp, nx)])
    return newton(y, temp_table, ny)

def find_4d_newton1(data, x, y, z, nx, ny, nz):
    x_list = data[0]
    y_list = data[1]
    z_list = data[2]
    data_list = data[3]
    temp = []
    i = 0
    for line in data_list:
        temp.append([z_list[i]])
        temp[i].append(find_3d_newton1(line, x_list, y_list, x, y, nx, ny))
        i += 1
    return newton(z, temp, nz)
