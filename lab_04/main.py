from input_output import *
from one_approc import *
from two_approc import *
from task_3 import *

n = 3

def create_x_y_z_w(data):
    xs = list()
    ys = list()
    zs = list()
    ws = list()
    for p in data:
        xs.append(p[0])
        ys.append(p[1])
        zs.append(p[2])
        ws.append(p[3])
    return np.array(xs), np.array(ys), np.array(zs), np.array(ws)


def error(data, func):
    nx, ny, nw = create_x_y_z(data)
    ne = []
    I = 0
    I_sum = 0
    for i in range(len(nx)):
        R = (func(nx[i]) - ny[i])
        I = nw[i] * R ** 2
        ne.append(I)
        I_sum += I
    return ne, I_sum

def error1(data, func):
    nx, ny, nz, nw = create_x_y_z_w(data)
    ne = []
    I = 0
    I_sum = 0
    for i in range(len(nx)):
        R = (func(nx[i], ny[i]) - nz[i])
        I = nw[i] * R ** 2
        ne.append(I)
        I_sum += I
    return ne, I_sum



choose = int(input("Выберите номер задания: "))
if (choose == 1):
    data = read_table("./data/tmp1.txt", 0)
    data1 = []
    for i in range(len(data)):
        data1.append(data[i])
        data1[i][2] = 1
    data = read_table("./data/tmp1.txt", 0)
    func = leastSquaresMethod_1D(data, n + 1)
    func1 = leastSquaresMethod_1D(data1, n + 1)
    drawGrafic1(func, func1, data)
    er, sum = error(data, func)
    print("Sum_I: ", sum)

elif (choose == 2):
    data = read_table("./data/tmp3.txt", 1)
    func = leastSquaresMethod_2D(data, n + 1)
    drawGrafic_2D(func, data, n + 1)
    er, sum = error1(data, func)
    print("Sum_I: ", sum)

elif (choose == 3):
    xp = np.linspace(-0.5, 2, 100)
    func, res1 = approc(xp, f, [c0, c1, c2])
    func2, res2 = approc(xp, f, [c0, c1, c2, c3])
    func3, res3 = approc(xp, f, [c0, c1, c2, c3, c4])
    print(np.round(res1, 2))
    print(np.round(res2, 2))
    print(np.round(res3, 2))
    drawGrafic(func, func2, func3, xp)
    

