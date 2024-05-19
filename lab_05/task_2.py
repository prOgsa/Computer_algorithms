import math as m
import numpy as np
import plotly.express as px

def integral_middle_method(interval, func):
    n = len(interval)
    a = interval[0]
    b = interval[n - 1]
    h = (b - a) / n

    return h * sum([func(interval[i] + h / 2) for i in range(n - 1)])

def Laplas(x, count = 100, method = integral_middle_method):
    def integral(x):
        return m.exp(-x ** 2 / 2)
    interval = np.linspace(0, x, count)
    return 2 / m.sqrt(2 * m.pi) * method(interval, integral)

def half_division(f, y, a, b, max_iteration, eps = 1e-8):
    n = 1
    while True:
        c = (a + b) / 2
        if abs(f(c) - y) < eps or n == max_iteration:
            return c, n
        if (f(a) - y) * (f(c) - y) < 0:
            b = c
        else:
            a = c
        n += 1

# x = np.linspace(-100, 100, 1000)
# y = [Laplas(i) for i in x]

# y_pred = np.linspace(-0.999999, 0.999999, 50)
# x_pred = [half_division(Laplas, y, min(x), max(x), 30, eps=1e-8)[0] for y in y_pred]

# fig = px.line(x=x, y=y)

# fig.add_scatter(x=x_pred, y=y_pred, mode='markers', name='HalfDivision')

res, iteration = half_division(Laplas, 0.56766, -10, 10, 200)
print(f"Аргумент функции Лапласа: {res}, iter = {iteration}")
# fig.show()