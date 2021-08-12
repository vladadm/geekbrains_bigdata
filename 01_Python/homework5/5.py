#!python3
# -*- coding: utf-8 -*-

import random

filename = '5_file.txt'


def gen_number_string(count):
    return " ".join([str(random.randint(0, 100)) for x in range(count)])


def write_data(datafile, data):
    with open(datafile, "w") as file:
        file.write(data)
    print("Save line: {} \nin file: {}.".format(data, datafile))


def read_file(datafile):
    with open(datafile, 'r',) as data:
        return data.read()


if __name__ == "__main__":
    write_data(filename, gen_number_string(100))
    # sum numbers from file
    print("Sum all numbers: {}".format(sum([int(x) for x in read_file(filename).split()])))
