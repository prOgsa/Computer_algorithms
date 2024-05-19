import numpy as np
import math as m
def f1(x, y, z):
    return x ** 2 + y ** 2 + z ** 2 - 1

def f2(x, y, z):
    return 2 * x ** 2 + y ** 2 - 4 * z

def f3(x, y, z):
    return 3 * x ** 2 - 4 * y + z ** 2

def jakobi_matrix(x, y, z):
    return [
        [2 * x, 2 * y, 2 * z],
        [4 * x, 2 * y, -4],
        [6 * x, -4, 2 * z]
    ]
x = -100
y = 1
z = 1200
coord = [x, y, z]
def create_triangle_matrix(data, n):
    for k in range(n):
        for i in range(k + 1, n):
            coeff = -(data[i][k] / data[k][k])
            for j in range(k, n + 1):
                data[i][j] += coeff * data[k][j]
    return data

def Gauss(data):
    n = len(data)
    triangle_data = create_triangle_matrix(data, n)

    result = np.zeros(n)
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            data[i][n] -= result[j] * data[i][j]
        result[i] = data[i][n] / data[i][i]
    return result

def newton(jakobi_matrix, func, coord, max_iteration, eps):
    def f(x):
        return [f(*x) for f in func]
    coord_tmp = coord
    n = 1
    while True:
        J = jakobi_matrix(*coord_tmp)
        b = [-f_val for f_val in f(coord_tmp)]
        
        for i in range(len(J)):
            J[i].append(b[i])
        
        dx = Gauss(J) 
        xnext = [coord_tmp[i] + dx[i] for i in range(len(coord_tmp))]
        if m.sqrt(sum([x ** 2 for x in dx])) < eps or n == max_iteration:
            return xnext, n
        coord_tmp = xnext
        n += 1

res, iteration = newton(jakobi_matrix, [f1, f2, f3], coord, 20, 1e-8)
print(f"Pешение системы уравнений при x0 = {x}, y0 = {y}, z0 = {z}: {res}, iter = {iteration}")
