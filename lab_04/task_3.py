from one_approc import *

def f(x, j):
    return x ** j * (1 - x)

def f0(x):
    return 1 - x

def f1(x):
    return x * (1 - x)

def f2(x):
    return x ** 2 * (1 - x)

def f3(x):
    return x ** 3 * (1 - x)

def f4(x):
    return x ** 4 * (1 - x)

def c0(x):
    return 1 - 4 * x

def c1(x):
    return - 2 + 2 * x - 3 * x ** 2

def c2(x):
    return 2 - 6 * x + 3 * x ** 2 - 4 * x ** 3

def c3(x):
    return 6 * x - 12 * x ** 2 + 4 * x ** 3 - 5 * x ** 4

def c4(x):
    return 12 * x ** 2 - 20 * x ** 3 + 5 * x ** 4 + 6 * x ** 5

def approc(xp, f, coef):
    n = len(coef) - 1
    data = np.zeros((n, n + 1))
    i = 0
    for f1 in coef[1:]:
        j = 0
        for f2 in coef[1:]:
            for x in xp:
                data[i][j] += f1(x) * f2(x)
            j += 1
        for x in xp:
            data[i][n] -= coef[0](x) * f1(x)
        i += 1
    result = Gauss(data)
    def f_res(x):
        return f(x, 0) + sum([result[i] * f(x, i + 1) for i in range(n)])
    return f_res, result

def drawGrafic(func, func1, func2, xValues):

    plt.ylabel("Y")
    plt.xlabel("X")
    xp = np.linspace(-0.5, 2, 100)

    yValues = [func(x) for x in xp]
    yValues1 = [func1(x) for x in xp]
    yValues2 = [func2(x) for x in xp]
    plt.plot(xValues, yValues, 'r', label="y = f(x)")
    plt.plot(xValues, yValues1, 'b', label="y = f(x)")
    plt.plot(xValues, yValues2, 'g', label="y = f(x)")
    plt.legend()
    plt.show()
