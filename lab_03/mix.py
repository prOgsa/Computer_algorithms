from newton import newton, find_3d_newton
from spline import spline, find_3d_spline
import numpy as np

def find_mixed_x_3d(data, x, y, nx, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, newton(x, temp, nx)])
    return spline(temp_table, y, start, end)

def find_mixed_x_4d(data, x, y, z, nx, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_mixed_x_3d(line[1], x, y, nx, start, end))
        i += 1 
    return spline(temp, z, start, end)

def find_mixed_y_3d(data, x, y, ny, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, newton(y, temp, ny)])
    return spline(temp_table, x, start, end)

def find_mixed_y_4d(data, x, y, z, ny, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_mixed_y_3d(line[1], x, y, ny, start, end))
        i += 1 
    return spline(temp, z, start, end)

def find_mixed_z_3d(data, x, y, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, spline(temp, x, start, end)])
    return spline(temp_table, y, start, end)

def find_mixed_z_4d(data, x, y, z, nz, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_mixed_z_3d(line[1], x, y, start, end))
        i += 1 
    return newton(z, temp, nz)

def find_mixed_xy_4d(data, x, y, z, nx, ny, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_3d_newton(line[1], x, y, nx, ny))
        i += 1 
    return spline(temp, z, start, end)

def find_mixed_xz_3d(data, x, y, nx, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, newton(x, temp, nx)])
    return spline(temp_table, y, start, end)

def find_mixed_xz_4d(data, x, y, z, nx, nz, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_mixed_xz_3d(line[1], x, y, nx, start, end))
        i += 1 
    return newton(z, temp, nz)

def find_mixed_yz_3d(data, x, y, ny, start, end):
    temp_table = []
    tmp = data
    for j in range(len(tmp[0])):
        temp = []
        for k in range(len(tmp)):
            temp.append([k, tmp[k][j]])
        temp_table.append([j, newton(y, temp, ny)])
    return spline(temp_table, x, start, end)

def find_mixed_yz_4d(data, x, y, z, ny, nz, start, end):
    temp = []
    i = 0
    for line in data:
        temp.append([line[0]])
        temp[i].append(find_mixed_yz_3d(line[1], x, y, ny, start, end))
        i += 1 
    return newton(z, temp, nz)