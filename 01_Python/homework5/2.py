#!python3
# -*- coding: utf-8 -*-

filename = '1_file.txt'

with open(filename, 'r') as file:
    data = file.readlines()
    print(f'В файле {filename} строк: {len(data)}')
    count = 0
    for line in data:
        count +=1
        print(f'Длинна строки {count}: {len(line)}')