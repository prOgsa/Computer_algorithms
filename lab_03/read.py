import re

def read_data(name_file):
    data = []
    i = 0
    j = 0
    with open(name_file, 'r') as f:
        for line in f:
            if "z=" in line:
                numbers = re.findall(r'\b\d+\.\d+|\b\d+\b', line)
                if numbers:
                    data.append([int(numbers[0]), []])
                    j += 1
                i = 1
            elif line:
                if i > 2:
                    numbers = re.findall(r'\b\d+\.\d+|\b\d+\b', line)
                    if numbers:
                        for i in range(len(numbers)):
                            numbers[i] = int(numbers[i])
                        data[j - 1][1].append(numbers[1:])
            i += 1
    return data

data = read_data("./data/data.txt")

def read_data1(name_file):
    data = []
    i = 0
    j = 0
    with open(name_file, 'r') as f:
        for line in f:
            if "z=" in line:
                j += 1
                data.append([])
                i = 0
            elif line:
                if i > 1:
                    numbers = re.findall(r'\b\d+\.\d+|\b\d+\b', line)
                    if numbers:
                        for i in range(len(numbers)):
                            numbers[i] = int(numbers[i])
                        data[j - 1].append(numbers[1:])
            i += 1
    return data