#!python3
# -*- coding: utf-8 -*-

filename = '1_file.txt'

with open(filename, 'w') as file:
    print(f"Create or rewrite file {filename}")
    while True:
        string = str(input("Input data: "))
        if not string:
            print(f'User input empty line, close file {filename}.')
            break
        file.write(f'{string}\n')
        print(f'Write in file: {string}')

