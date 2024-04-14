def find_points(x, n, x_data, y_data):
    ind = 0
    while ind < len(x_data) and x > x_data[ind]:
        ind += 1
    ind -= 1 if ind != 0 else 0

    i = 0
    min_i = ind
    max_i = ind
    chose_min = True
    while i < n:
        if max_i < len(x_data) and not chose_min:
            max_i += 1
            chose_min = True
        elif not chose_min:
            min_i = 1
            chose_min = True

        elif min_i > 0 and chose_min:
            min_i -= 1
            chose_min = False
        elif chose_min:
            max_i += 1
            chose_min = False
        
        i += 1

    return min_i, max_i

def divided_difference1(x_data, y_data, n):
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
    result = divided_difference1(x_data, y_data, n)
    y = 0
    for i in range(n + 1):
        tmp = 1
        for j in range(i):
            tmp *= (x - x_data[j])
        y += result[i] * tmp
    return y

def divided_difference(mat):
    diff_mat = [[row[1] for row in mat]]
    for i in range(1, len(mat)):
        tmp = []
        for j in range(len(mat) - i):
            tmp.append((diff_mat[i - 1][j + 1] - diff_mat[i - 1][j]) / (mat[i + j][0] - mat[j][0]))
        diff_mat.append(tmp)
    return diff_mat


def second_derivative_newton(x, data):
    x_data = [row[0] for row in data]
    y_data = [row[1] for row in data]
    n = 3
    min_i, max_i = find_points(x, n, x_data, y_data)
    new_data = data[min_i:max_i + 1]
    diff_table = divided_difference(new_data)
    return 2 * diff_table[2][0] + diff_table[3][0] * (6 * x - 2 * (new_data[0][0] + new_data[1][0] + new_data[2][0]))