#!python3
# -*- coding: utf-8 -*-

filename = '3_students.txt'


def load_students_salary():
    with open(filename, 'r') as file:
        data = file.readlines()
        students_dict = {}
        for line in data:
            name, salary = line.split(":")
            students_dict.update({name.strip(): int(salary.strip())})

    print(students_dict)
    return students_dict


students = load_students_salary()


for student in students:
    if students.get(student) < 20000:
        print(student)
