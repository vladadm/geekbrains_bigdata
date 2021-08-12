#!python3
# -*- coding: utf-8 -*-


class Matrix:
    def __init__(self, matrix_list):
        self.mtx = matrix_list

    def __str__(self):
        return_line = ""
        for row in range(len(self.mtx)):
            for el in range(len(self.mtx[row])):
                return_line += f"{self.mtx[row][el]} "
            return_line += "\n"
        return return_line

    def __add__(self, other):
        temp_list = []
        for row in range(len(self.mtx)):
            temp_list.append([])
            for el in range(len(self.mtx[row])):
                temp_list[row].append(self.mtx[row][el] + other.mtx[row][el])
        self.mtx = temp_list



if __name__ == "__main__":
    mtx = Matrix([[1, 7, 3], [5, 5, 5], [3, 3, 3]])
    print(mtx)
    mtx1 = Matrix([[2, 2, 4], [1, 1, 1], [4, 2, 6]])
    print(mtx1)
    mtx.__add__(mtx1)
    print(mtx)
