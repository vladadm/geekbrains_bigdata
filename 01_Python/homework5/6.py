#!python3
# -*- coding: utf-8 -*-

import re

filename = '6_file.txt'

dict_ = {}


def read_file(datafile):
    with open(datafile, 'r',) as data:
        return data.readlines()


def splitter(data):
    """
    :list
    Функция преобразует строку в словарь по формату:
    Урок: кол-во занятий
    :return dict
    """
    subj_dict = {}
    for line in data:
        subject, lessons = line.split(":")
        subj_dict.update({subject: sum([int(x) for x in re.findall(r'\d+', lessons)])})
    return subj_dict


if __name__ == "__main__":
    print(splitter(read_file(filename)))

