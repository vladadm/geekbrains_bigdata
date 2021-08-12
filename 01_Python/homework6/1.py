#!python3
# -*- coding: utf-8 -*-

import time


class TrafficLight:
    def __init__(self):
        self.__color = ""

    def running(self, worktime):
        running_time = worktime
        print(f"Светофор запущен на {worktime}сек.")
        while worktime > 0:
            self.__color = "red"
            print(f"Цвет светофора: {self.__color}")
            time.sleep(7)
            worktime -= 7
            self.__color = "yellow"
            print(f"Цвет светофора: {self.__color}")
            time.sleep(2)
            worktime -= 2
            self.__color = "green"
            print(f"Цвет светофора: {self.__color}")
            time.sleep(10)
            worktime -= 10
        print("TrafficLight  is turn off")


if __name__ == "__main__":
    tl = TrafficLight()
    tl.running(20)
