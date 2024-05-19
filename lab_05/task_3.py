import numpy as np
from matplotlib import pyplot as plt

x1 = 0
y1 = 1
x2 = 1
y2 = 3

N = 10
h = (x2 - x1) / N
x = np.linspace(x1, x2, N + 1)

def start_y(x):
    return x ** 2 + x + 1

y = [start_y(xp) for xp in x]

def jakobi_matrix(y):
    n = len(y)
    res = np.zeros((n, n))
    res[0][0] = 1
    for i in range(1, n - 1):
            res[i][i - 1] = 1 / h ** 2
            res[i][i] = -2 / h ** 2 - 3 * y[i] ** 2
            res[i][i + 1] = 1 / h ** 2
    res[n - 1][n - 1] = 1
    return res

def func(n):
    n = int(n)
    if n == 0:
        def count(*y):
            return y[0] - y1
    elif n == N:
        def count(*y):
            return y[n] - y2
    else:
        def count(*y):
            return (y[n - 1] + -2 * y[n] + y[n + 1]) / h ** 2 - y[n] ** 3 - x[n]**2
    return count
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
        J = jakobi_matrix(coord_tmp)
        b = [-f_val for f_val in f(coord_tmp)]
        
        J = np.column_stack((J, b))
        dx = Gauss(J) 
        xnext = [coord_tmp[i] + dx[i] for i in range(len(coord_tmp))]
        if np.sqrt(sum([x ** 2 for x in dx])) < eps or n == max_iteration:
            return xnext, n
        coord_tmp = xnext
        n += 1
funcs = [func(i) for i in range(N + 1)]

res, i = newton(jakobi_matrix, funcs, y, 30, 1e-8)
# print("Решение уравнения:", res)

plt.figure("График функции")
plt.ylabel("Y")
plt.xlabel("X")

plt.plot(x, res, 'r', label="y(x)")

plt.legend()
plt.show()