from read import read_data, read_data1
from prettytable import PrettyTable
from newton import *
from spline import find_4d_spline
from mix import *
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = read_data("./data/data.txt")

x = 1.5
y = 1.5
z = 1.5

nx = 2
ny = 2
nz = 2

def get_info():
    print("Введите значения для которых выполняется интерполяция:")
    x = float(input("Введите х: "))
    y = float(input("Введите y: "))
    z = float(input("Введите z: "))
    
    print("\nВыберите способ интерполяции:")
    print("1. Полиномами Ньютона")
    print("2. Сплайнами")
    print("3. Смешанной интерполяцией")
    choose = int(input())
    if choose == 3:
        print("4. Смешанная интерполяция по x")
        print("5. Смешанная интерполяция по y")
        print("6. Смешанная интерполяция по z")
        print("7. Смешанная интерполяция по xy")
        print("8. Смешанная интерполяция по xz")
        print("9. Смешанная интерполяция по yz")
        choose = int(input())

    if choose != 2:
        print("\nВведите степени аппроксимации:")
        nx = int(input("Введите nx: "))
        ny = int(input("Введите ny: "))
        nz = int(input("Введите nz: "))

def print_table(data):
    for line in data:
        print(f"z = {line[0]}")
        table = PrettyTable()
        length = len(line[1])
        table.field_names = ["Y / X"] + [str(i) for i in range(length)]
        j = 0
        for row in line[1]:
            strings = list(map(str, row))
            table.add_row([f'{j}'] + strings)
            j += 1
        print(table)
def print_answer(data, x, y, z, nx, ny, nz):
    print(f"Результат интерполяции полиномом Нютона в заданной точке:", find_4d_newton(data, x, y, z, nx, ny, nz))
    print(f"Результат интерполяции сплайнам в заданной точке:", find_4d_spline(data, x, y, z, 0, 0))
    print(f"Результат смешанной интерполяции по x в заданной точке:", find_mixed_x_4d(data, x, y, z, nx, 0, 0))
    print(f"Результат смешанной интерполяции по y в заданной точке:", find_mixed_y_4d(data, x, y, z, ny, 0, 0))
    print(f"Результат смешанной интерполяции по z в заданной точке:", find_mixed_z_4d(data, x, y, z, nz, 0, 0))
    print(f"Результат смешанной интерполяции по xy в заданной точке:", find_mixed_xy_4d(data, x, y, z, nx, ny, 0, 0))
    print(f"Результат смешанной интерполяции по xz в заданной точке:", find_mixed_xz_4d(data, x, y, z, nx, nz, 0, 0))
    print(f"Результат смешанной интерполяции по yz в заданной точке:", find_mixed_yz_4d(data, x, y, z, ny, nz, 0, 0))
print_answer(data, x, y, z, nx, ny, nz)

data_z1 = np.array(data[round(z)][1])

# z = find_4d_newton(data, x, y, z, nx, ny, nz)

steps = 20
Ymax = 4
Xmax = 4
Ymin = 0
Xmin = 0

dy = (Ymax - Ymin) / steps
dx = (Xmax - Xmin) / steps

x_arr = [Xmin + dx * i for i in range(steps + 1)]
y_arr = [Ymin + dy * i for i in range(steps + 1)]

newtonfarr = ([[find_4d_newton(data, x, y, z, nx, ny, nz) for y in y_arr] for x in x_arr])
# splinefarr = ([[find_4d_spline(data, x, y, z, 0, 0) for y in y_arr] for x in x_arr])
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


x_1 = [0, 1, 2, 3, 4]
y_1 = [0, 1, 2, 3, 4]
x_1, y_1 = np.meshgrid(x_1, y_1)
# z = np.cos(x_1) ** 2 + np.sin(y_1) ** 2

x_arr = np.array(x_arr)
y_arr = np.array(y_arr)
x_arr, y_arr = np.meshgrid(x_arr, y_arr)

newtonfarr = np.array(newtonfarr)
# splinefarr = np.array(splinefarr)

# x_2, y_2 = np.meshgrid(x_arr, y_arr)
# z = np.cos(x_2) ** 2 + np.sin(y_2) ** 2

xb, xe, nx = -5, 5, 20
yb, ye, ny = -3, 4, 50
zb, ze, nz = -1, 2, 30

x = np.linspace(xb, xe, nx)
y = np.linspace(yb, ye, ny)
z = np.linspace(zb, ze, nz)

def f(x, y, z):
    return np.exp(2 * x - y) * z ** 2
data = []
data.append(x)
data.append(y)
data.append(z)
u = np.zeros((nz, ny, nx))
for k in range(nz):
    for j in range(ny):
        for i in range(nx):
            u[k, j, i] = f(x[i], y[j], z[k])
X = -0.152
Y = 1.141
Z = 1.43
xs = 2
ys = 2
zs = 2
data.append(u)

print("u = f(x, y, z):", find_4d_newton1(data, X, Y, Z, xs, ys, zs))
print("f(x, y, z):", f(X, Y, Z))

# u = np.zeros((ny, nx))

# x, y, z = np.meshgrid(x, y, z)
# colors = plt.cm.viridis(u)
surf = ax.plot_surface(x_1, y_1, data_z1, cmap='plasma', rstride=1, cstride=1, label=f'z={z}', antialiased=True)
# surf = ax.plot_surface(x_arr, y_arr, newtonfarr, cmap='plasma', rstride=1, cstride=1)
# fig = go.Figure(
#     go.Surface(x=x, y=y, z=u)
# )
# surf = ax.plot_surface(y,x, u, cmap='plasma', rstride=1, cstride=1)
# fig.show()

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')

fig.colorbar(surf)
plt.show()
