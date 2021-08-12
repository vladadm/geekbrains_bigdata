#!python3
# -*- coding: utf-8 -*-

class Car():
    def __init__(self, speed, color, name, is_police=False):
        self.speed = int(speed)
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        print(f"Машина: {self.name} поехала")

    def stop(self):
        print(f"Машина: {self.name} остановилась")

    def turn(self, direction):
        print(f"Машина: {self.name} повернула на {direction}")

    def show_speed(self):
        print(f"Машина: {self.name} скорость {self.speed}")


class TownCar(Car):
    def car_type(self):
        print('TownCar')

    def show_speed(self):
        if self.speed > 60:
            print(f"Машина: {self.name} превышение скорости: {self.speed}")
        else:
            print(f"Машина: {self.name} скорость {self.speed}")


class WorkCar(Car):
    def car_type(self):
        print('WorkCar')

    def show_speed(self):
        if self.speed > 40:
            print(f"Машина: {self.name} превышение скорости: {self.speed}")
        else:
            print(f"Машина: {self.name} скорость {self.speed}")


class SportCar(Car):
    def car_type(self):
        print('SportCar')


class PoliceCar(Car):
    def car_type(self):
        print('PoliceCar')


if __name__ == "__main__":
    fiat = TownCar('50', 'green', 'Fiat')
    fiat.turn('лево')
    fiat.show_speed()
    fiat.speed = 70
    fiat.show_speed()
    print()
    gazel = WorkCar('30', 'yellow', 'Gazel')
    gazel.turn('право')
    gazel.show_speed()
    gazel.speed = 50
    gazel.show_speed()
    print()
    ferrari = SportCar('200', 'red', 'Ferrari')
    ferrari.go()
    ferrari.show_speed()
    ferrari.turn('право')
    ferrari.stop()
    print()
    police = PoliceCar('150', 'black', 'Chevrolet', True)
    police.go()
    print(f"Машина {police.name} полицейская машина: {police.is_police}")
    police.show_speed()
    police.turn('право')
    police.turn('лево')

