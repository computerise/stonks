from csv import DictReader
from json import dump


def convert_csv_to_json(
    input_csv_path: str = "raw.csv", output_json_path: str = "input.json"
):
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


if __name__ == "__main__":
    convert_csv_to_json()
