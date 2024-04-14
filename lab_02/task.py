import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from newton import newton, second_derivative_newton

def read_from_file_to_list(name_file):
    data = []
    with open(name_file, 'r') as f:
        for line in f:
            elem = line.split()
            elem = [float(e) for e in elem]
            data.append(elem)
    data = sorted(data, key=lambda x: x[0])
    return data


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

data = read_from_file_to_list("data/data.txt")
X = 1.6657
print("X = ", X)
print("Полином Ньютона 3-й степени: ", newton(X, data, 3))
print("Сплайн естественного порядка: ", spline(data, X, 0, 0))

x = [i[0] for i in data]
q = []
q1 = []
q2, q3 = [], []
l1 = second_derivative_newton(min(x), data)
l2 = second_derivative_newton(max(x), data)
print("Сплайн P'' и 0: ", spline(data, X, l1, 0))
print("Сплайн P'' и P'': ", spline(data, X, l1, l2))

x_beg = x[0]
xi = x_beg
x_step = 1e-3
x_list = []
while xi < x[-1]:
    x_list.append(xi)
    q.append(spline(data, xi, 0, 0))
    q1.append(newton(xi, data, 3))
    q2.append(spline(data, xi, l1, 0))
    q3.append(spline(data, xi, l1, l2))
    xi += x_step
plt.plot(x_list, q, '-', color='r', label='Сплайн естественного порядка')
plt.plot(x_list, q1, '-', color='g', label='Полином Ньютона 3-й степени')
plt.plot(x_list, q2, '-', color='b', label="Сплайн P'' и 0")
plt.plot(x_list, q3, '-', color='pink', label="Сплайн P'' и P''")
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()