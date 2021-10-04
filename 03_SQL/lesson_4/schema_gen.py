#!python3
# -*- coding: utf-8 -*-


class DataGenerator:
    def __init__(self, line_count):
        self.lineCount = int(line_count)

    def generate(self, table_name):
        dbname = "vk"
        table_name = "users"
        for line in range(0, self.lineCount):
            print("INSERT INTO {}.{} VALUES({}".format(dbname, table_name, self.values()))

    def values(self):
        return "()"



if __name__ == "__main__":
    data = DataGenerator(20).generate()
