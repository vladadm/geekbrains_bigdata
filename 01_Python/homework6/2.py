#!python3
# -*- coding: utf-8 -*-


class Road:
    def __init__(self, lenght, width):
        self.__length = lenght
        self.__width = width

    def calc_mass(self, mass, layer):
        print(f"Массы асфальта: {self.__length * self.__width * mass * layer}")


if __name__ == "__main__":
    road1 = Road(20, 5000)
    road1.calc_mass(25, 5)
    road2 = Road(70, 100)
    road2.calc_mass(10, 5)
