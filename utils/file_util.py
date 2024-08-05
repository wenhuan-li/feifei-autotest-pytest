import csv


def get_csv_datas(file_path, scope):
    with open(file_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return [row for row in reader
                if row.get("scope") != "skip" and row.get("scope") in scope]
