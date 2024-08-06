import csv


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
