#!python3
# -*- coding: utf-8 -*-

filename = '4_file.txt'
filename_new = '4_file_new.txt'


def read_file(datafile):
    with open(datafile, 'r',) as file:
        data = file.readlines()

    return data


def modify_data(data):
    numbers = {
        '1': 'Один',
        '2': 'Два',
        '3': 'Три',
        '4': 'Четыре',
    }
    new_data = []
    for line in data:
        line = line.strip()
        print(line)
        print(line.split(" "))
        _, _, number = line.split(" ")
        print(number, numbers.get(number))
        new_data.append(line.replace(number, numbers.get(number)+"\n"))

    print(new_data)
    return new_data


def write_data(datafile, data):
    with open(datafile, "w") as file:
        for line in data:
            file.write(line)
    print("File {} saved".format(datafile))


if __name__ == "__main__":
    new_data = modify_data(read_file(filename))
    write_data(filename_new, new_data)
