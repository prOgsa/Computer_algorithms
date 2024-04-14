import numpy as np
def find_e(e, h1, h2):
    return - h1 / (h2 * e + 2 * (h1 + h2))
    
def find_nu(dy1, dy2, h1, h2, nu, e):
    return (3 * (dy1 / h1 - dy2 / h2) - h2 * nu) / (h2 * e + 2 * (h1 + h2))

def spline(data, x, start, end):
    n = len(data)
    k = 0
    while k < n - 2 and x > data[k + 1][0]:
        k += 1
    
    a = np.zeros(n - 1)
    b = np.zeros(n - 1)
    c = np.zeros(n - 1)
    d = np.zeros(n - 1)
    h = np.zeros(n)
    e = np.zeros(n)
    nu = np.zeros(n)
    # A ???
    for i in range(1, n):
        a[i - 1] = data[i - 1][1] 
    # h
    for i in range(1, n - 1):
        h[i] = data[i + 1][0] - data[i][0]

    # C
    c[0] = start / 2
    e[1] = 0
    nu[1] = start / 2
    for i in range(2, n):
        h_i = data[i][0] - data[i - 1][0]
        h_i1 = data[i - 1][0] - data[i - 2][0]

        e[i] = find_e(e[i - 1], h_i, h_i1)
        dy = data[i][1] - data[i - 1][1]
        dy1 = data[i - 1][1] - data[i - 2][1]
        nu[i] = find_nu(dy, dy1, h_i, h_i1, nu[i - 1], e[i - 1])

    c[-1] = nu[-1] + (end / 2) * e[-1]
    for i in range(n - 2, 0, -1):
        c[i - 1] = nu[i] + c[i] * e[i]
    # B
    for i in range(n - 2):
        h_i = (data[i + 1][0] - data[i][0])
        b[i] = (data[i + 1][1] - data[i][1]) / h_i - 1 / 3 * (h_i * (c[i + 1] + 2 * c[i]))
    h_i = (data[-1][0] - data[-2][0])
    b[-1] = (data[-1][1] - data[-2][1]) / h_i - 1 / 3 * h_i * ((end / 2) + 2 * c[-1])

    # D
    for i in range(n - 2):
        d[i] = (c[i + 1] - c[i]) / (3 * (data[i + 1][0] - data[i][0]))
    d[-1] = ((end / 2) - c[-1]) / (3 * h_i)

    xi = data[k][0]
    return a[k] + b[k] * (x - xi) + c[k] * (x - xi) ** 2 + d[k] * (x - xi) ** 3

def find_3d_spline(data, x, y, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, spline(temp, x, start, end)])
    # print(temp_table)
    return spline(temp_table, y, start, end)

def find_4d_spline(data, x, y, z, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_3d_spline(line[1], x, y, start, end))
        i += 1 
    # print(temp)
    return spline(temp, z, start, end)
