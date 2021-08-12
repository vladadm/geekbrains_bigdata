#!python3
# -*- coding: utf-8 -*-

import json

filename = '7_file.txt'
json_filename = "7_file.json"


def read_file(datafile):
    with open(datafile, 'r') as data:
        return data.readlines()


def write_data(datafile, data):
    with open(datafile, "w") as file:
        file.write(data)
    print("Save line: {} \nin file: {}.".format(data, datafile))


def json_converter(data):
    """
    :return dict
    """

    unprofitable_companies = {"unprofitable": []}
    companies_profit = {}

    all_profit = []
    all_expense = []
    list_for_json = []

    for line in data:
        name, union, profit, expenses = line.strip().split(" ")
        all_profit.append(int(profit))
        all_expense.append(int(expenses))
        companies_profit.update({name: int(profit)})
        if int(expenses) >= int(profit):
            unprofitable_companies["unprofitable"].append({name: expenses})

    list_for_json.append(companies_profit)

    list_for_json.append({"average_profit": sum(all_profit)/len(all_profit)})
    list_for_json.append(unprofitable_companies)
    list_for_json.append({"all_costs": sum(all_expense)})

    #print(json.dumps(list_for_json, indent=4, ensure_ascii=False))

    return json.dumps(list_for_json, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    write_data(json_filename, json_converter(read_file(filename)))
