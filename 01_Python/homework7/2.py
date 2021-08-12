#!python3
# -*- coding: utf-8 -*-


class Clothes:
    def __init__(self, name, clothe, param):
        self.name = "Пальто"
        self.clothe = clothe
        self.param = param

    def __setattr__(self, key, value):
        name = self.name
        print(name)
        if key == 'name' and value == "Пальто":
            #self.__dict__['name'] = value
            print(f"Шьем: {value}") #для размера: {value} нужно ткани: {10/6.5+0.5}")

        if key == 'type' and value == "Костюм":
            self.__dict__['name'] = value
            print(f"Шьем: {self.name} для размера: {value} нужно ткани: {10 / 6.5 + 0.5}")

class Coat(Clothes):
    def __setattr__(self, key, value):
        self.name = name
        if key == 'name' and value == "Пальто":
            #self.__dict__['name'] = value
            print(f"Шьем: {value}") #для размера: {value} нужно ткани: {10/6.5+0.5}")

        if key == 'type' and value == "Костюм":
            self.__dict__['name'] = value
            print(f"Шьем: {self.name} для размера: {value} нужно ткани: {10 / 6.5 + 0.5}")

    @property
    def total_cloth(self):
        print(f"На {self.name} нужно ткани: {10/6.5+0.5}")

# class Costume(Clothes):
#
#     def total_cloth(self):
#         height/6.5 + 0.5


if __name__ == "__main__":
    coat = Clothes("Зимнее Пальто", "пальто", 20)
    # print(coat.name)
    # coat.size = 20
    # print(coat.size)
    #print(coat.param)
    #costume = Clothes("Спортивный костюм", "Костюм", 30)

    coat.total_cloth
