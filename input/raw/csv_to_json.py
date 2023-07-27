#! /usr/bin/env python3

from csv import DictReader
from pandas import read_csv
from json import dump


def convert_csv_to_json(input_csv_path: str = "ftse_all_share.csv", output_json_path: str = "ftse_all_share.json"):
    snake_cased = {}
    with open(input_csv_path) as csv_file:
        dict_reader = DictReader(csv_file)
        for company in dict_reader:
            for key, value in company.items():
                if key == "Symbol":
                    company_symbol = value
                    snake_cased[company_symbol] = {}
                else:
                    snake_case_key = key.lower().replace(" ", "_").replace("-", "_")
                    snake_cased[company_symbol][snake_case_key] = value
    with open(output_json_path, "w") as json_file:
        dump(snake_cased, json_file, indent=4)


def convert_ftse_to_json(input_csv_path: str = "ftse_all_share.csv", output_json_path: str = "ftse_all_share.json"):
    json = {}
    with open(input_csv_path) as csv_file:
        csv_data = read_csv(
            csv_file, index_col=False, delimiter="\t", header=0, names=["ticker", "name", "index", "price", "market_cap"]
        )
        for item in csv_data.values:
            json[item[0]] = {"name": item[1], "index": item[2], "price": item[3], "market_cap": item[4]}
    with open(output_json_path, "w") as json_file:
        dump(json, json_file, indent=4)


if __name__ == "__main__":
    convert_ftse_to_json()
