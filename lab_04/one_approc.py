import numpy as np
from input_output import *
from matplotlib import pyplot as plt

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


def makeSlau_1D(data, n):
    matrixSlau = [[0.0 for _ in range(n + 1)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            sums = 0
            for p in data:
                sums += p[2] * p[0]**(i + j)
            matrixSlau[i][j] = sums

        sums = 0
        for p in data:
            sums += p[2] * p[1] * p[0]**i
        matrixSlau[i][n] = sums

    return matrixSlau

def find_interval(data, ind):
    min_x = data[0][ind]
    max_x = data[0][ind]
    for line in data:
        if line[ind] < min_x:
            min_x = line[ind]
        if line[ind] > max_x:
            max_x = line[ind]
    return min_x, max_x

def leastSquaresMethod_1D(data, n):
    slau = makeSlau_1D(data, n)

    print("\nМатрица СЛАУ:")
    print_matrix(slau)
    aValues = Gauss(slau)

    print_result_coeff(aValues)

    def approximate_func(x):
        y = 0
        for i in range(len(aValues)):
            y += aValues[i] * x**i
        return y

    return approximate_func

def parse(data):
    xs = list()
    ys = list()
    ws = list()
    for p in data:
        xs.append(p[0])
        ys.append(p[1])
        ws.append(p[2])
    return np.array(xs), np.array(ys), np.array(ws)



def drawGrafic1(func, func1, data):
    xMin, xMax = find_interval(data, 0)
    xValues = np.linspace(xMin, xMax, 40)


    plt.figure("График(и) функции, полученный аппроксимации наименьших квадратов")
    plt.ylabel("Y")
    plt.xlabel("X")

    for p in data:
        plt.plot(p[0], p[1], 'r.')

    yValues = func(xValues)
    yValues1 = func1(xValues)
    plt.plot(xValues, yValues, 'r', label="y = f(x)")
    xs, ys, ws = parse(data)
    plt.plot(xValues, yValues1, 'b', label="y = f(x)")

    plt.legend()
    plt.show()

