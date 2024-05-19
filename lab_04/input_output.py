import re
from prettytable import PrettyTable
import numpy as np
from random import randint, random
from tabulate import tabulate


def read_table(name_file, flag):
    data = []
    with open(name_file, 'r') as f:
        for line in f:
            numbers = re.findall(r'-?\b\d+\.\d+|-?\b\d+\b', line)
            numbers = [float(num) for num in numbers]
            if (flag == 1):
                tmp = numbers[0]
                numbers[0] = numbers[2]
                numbers[2] = tmp
            data.append(numbers)
    return data


def print_table_1D(data):
    table = PrettyTable()
    table.field_names = ["№", "x", "y", "p"]
    i = 1
    for row in data:
        row.insert(0, i)
        table.add_row(row)
        i += 1
    print(table)

def print_table_2D(data):
    table = PrettyTable()
    table.field_names = ["№", "x", "y", "z", "p"]
    i = 1
    for row in data:
        row.insert(0, i)
        table.add_row(row)
        i += 1
    print(table)


def generate_table_1(f, start, end, amount):
    dataTable = []
    Xvalues = np.linspace(start, end, amount + 1)
    for x in Xvalues:
        x_val = round(x, 3)
        y_val = round(f(x), 3)
        p_val = randint(1, 5)
        dataTable.append([x_val, y_val, p_val])
    return dataTable


def generate_table_2(f, xstart, xend, ystart, yend, amount_x, amount_y):
    dataTable = []
    Xvalues = np.linspace(xstart, xend, amount_x)
    Yvalues = np.linspace(ystart, yend, amount_y)
    for i in range(amount_x):
        for j in range(amount_y):
            x_val = round(Xvalues[i], 3)
            y_val = round(Yvalues[j], 3)
            z_val = round(f(Xvalues[i], Yvalues[j]), 3)
            p_val = randint(1, 15)
            dataTable.append([x_val, y_val, z_val, p_val])
    return dataTable
     
def change_weight(data, i, num):
    data[i - 1][2] = num
    return data


def print_matrix(data):
    if isinstance(data, list):
        data = np.array(data)
    m, n = data.shape
    headers = [f"c{i}" for i in range(n - 1)] + ["f"]
    table = np.vstack([headers, data])
    print(tabulate(table, tablefmt="fancy_grid"))
    
def print_result_coeff(result):
    for i in range(len(result)):
        print(f"a{i} = {round(result[i], 5)}")
        
def print_SLAY(n):
    print("Система линейных алгебраических уравнений (СЛАУ)")
    for i in range(n):
        string = f"{i + 1}. "
        for j in range(n + 1):
            string += f"(x^{i}, x^{j}) * a{j}"
            if (j != n):
                string += " + "
            else:
                string += f" =  (y, x^{j})"
        print(string)
