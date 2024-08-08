import csv
import os.path

import pandas as pd


def get_csv_datas(file_path, scope):
    with open(file_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=',', quotechar='"')
        header = next(reader)
        datas = []
        for row in reader:
            row_dict = dict(zip(header, row))
            row_scope = row_dict.get("scope")
            if row_scope != "skip" and row_scope in scope:
                datas.append(row_dict)
        return datas


def pd_read_datas(file_path, sheet_name=None, columns=None):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == ".csv":
        df = pd.read_csv(file_path, quoting=csv.QUOTE_NONE, escapechar="\\")
    elif file_extension in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine="openpyxl")
    else:
        raise ValueError("Error! Unknown file type")
    if columns:
        df.rename(columns=columns, inplace=True)
    return df.to_dict(orient="records")
