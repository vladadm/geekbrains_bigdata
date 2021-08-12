#!python3
# -*- coding: utf-8 -*-


class Stationery:
    def __init__(self, title):
        self.title = title

    def draw(self):
        print("Запуск отрисовки")


class Pen(Stationery):
    """Ручка"""
    def draw(self):
        print(f"Тип изделия: {self.title}\nЗапуск отрисовки ручкой")


class Pencil(Stationery):
    """Карандаш"""
    def draw(self):
        print(f"Тип изделия: {self.title}\nПишем карандашом")


class Handle(Stationery):
    """Маркер"""
    def draw(self):
        print(f"Тип изделия: {self.title}\nРисуем маркером")


if __name__ == "__main__":
    marker = Handle('маркер')
    marker.draw()

    ruchka = Pen('ручка')
    ruchka.draw()

    karandash = Pencil('карандашь')
    karandash.draw()

