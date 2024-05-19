import numpy as np
from input_output import *
from one_approc import *
from matplotlib import pyplot as plt

def find_n_2D(n):
    return int((n + 1) * (n + 2) / 2)

def getValue(x, y, powx, powy):
    return x ** powx * y ** powy

def makeSlau_2D(data, n):
    a = list()
    b = list()
    for i in range(n + 1):
        for j in range(n + 1 - i):
            a_row = []
            for k in range(n + 1):
                for t in range(n + 1 - k):
                    a_row.append(sum(list(map(
                                lambda p: getValue(p[0], p[1], k + i, t + j) * p[3], data))))
            a.append(a_row)
            b.append(sum(list(map(
                            lambda p: getValue(p[0], p[1], i, j) * p[2] * p[3], data))))
    data = list()
    for i in range(len(a)):
       data.append(a[i])
       data[i].append(b[i])
    return data


def leastSquaresMethod_2D(data, n=1):
    slau = makeSlau_2D(data, n)
    print("\nМатрица СЛАУ:")
    print_matrix(slau)

    c = Gauss(slau)
    print_result_coeff(c)

    def approximate_func(x, y):
        result = 0
        ind = 0
        for i in range(n + 1):
            for j in range(n + 1 - i):
                result += c[ind] * getValue(x, y, i, j)
                ind += 1
        return result

    return approximate_func

def create_x_y_z(data):
    xs = list()
    ys = list()
    zs = list()
    for p in data:
        xs.append(p[0])
        ys.append(p[1])
        zs.append(p[2])
    return np.array(xs), np.array(ys), np.array(zs)


def drawGrafic_2D(func, data, n):
    minX, maxX = find_interval(data, 0)
    minY, maxY = find_interval(data, 1)

    xValues = np.linspace(minX, maxX, 40)
    yValues = np.linspace(minY, maxY, 40)
    zValues = [func(xValues[i], yValues[i]) for i in range(len(xValues))]

    def make_2D_matrix():
        # Создаем двумерную матрицу-сетку
        xGrid, yGrid = np.meshgrid(xValues, yValues)
        zGrid = np.array([[func(xGrid[i][j], yGrid[i][j]) for j in range(len(xValues))] for i in range(len(yValues))])
        return xGrid, yGrid, zGrid


    fig = plt.figure("График функции, полученный аппроксимации наименьших квадратов")
    xpoints, ypoints, zpoints = create_x_y_z(data)
    axes = fig.add_subplot(projection='3d')
    axes.scatter(xpoints, ypoints, zpoints, c='red')
    axes.set_xlabel('OX')
    axes.set_ylabel('OY')
    axes.set_zlabel('OZ')
    xValues, yValues, zValues = make_2D_matrix()
    axes.plot_surface(xValues, yValues, zValues)
    plt.show()