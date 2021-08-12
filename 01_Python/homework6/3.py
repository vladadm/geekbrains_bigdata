#!python3
# -*- coding: utf-8 -*-


class Worker:
    def __init__(self, name, surname, position):
        self.name = name
        self.surname = surname
        self.position = position
        self.__income = {"wage": 100000, "bonus": 50000}


class Position(Worker):
    def get_full_name(self):
        print(f"Полное имя сотрудника: {self.name} {self.surname}")

    def get_total_income(self):
        print(f"Полный доход: {int(self._Worker__income.get('wage')) + int(self._Worker__income.get('bonus'))}")


if __name__ == "__main__":
    p0 = Position('vasiliy', 'petrov', 'specialist')
    p0.get_full_name()
    p0.get_total_income()

    p1 = Position('andrey', 'ivanov', 'TeamLead')
    p1.get_full_name()
    p1.get_total_income()
