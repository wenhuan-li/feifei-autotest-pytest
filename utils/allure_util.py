import json
import os
import subprocess


def get_max_build_no(data_json):
    if not data_json:
        return 0
    last_element = data_json[-1]
    return last_element.get("buildOrder", 0)


class AllureUtil:

    def __init__(self, root_dir, allure_dir):
        self.root_dir = root_dir
        self.allure_dir = allure_dir
        self.allure_html = os.path.join(allure_dir, "html")
        self.data_json = []
        self.max_build = 0

    def add_executors(self):
        allure_file = os.path.join(self.root_dir, "assets", "executor.json")
        os.system(f"copy /Y {allure_file} {self.allure_dir}")

    def add_categories(self):
        allure_file = os.path.join(self.root_dir, "assets", "categories.json")
        os.system(f"copy /Y {allure_file} {self.allure_dir}")

    def add_environment(self):
        allure_file = os.path.join(self.root_dir, "assets", "environment.properties")
        os.system(f"copy /Y {allure_file} {self.allure_dir}")

    def generate_report(self):
        os.system(f"allure generate {self.allure_dir} -o {self.allure_html} --clean")

    def change_windows_title(self, title):
        with open(os.path.join(self.allure_html, "index.html"), "r+", encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            for line in lines:
                file.write(line.replace("Allure Report", title))

    def change_summary_title(self, title):
        with open(os.path.join(self.allure_html, "widgets", "summary.json"), "rb") as file:
            params = json.load(file)
            params["reportName"] = title
            new_params = params
        with open(os.path.join(self.allure_html, "widgets", "summary.json"), "w", encoding="utf-8") as file:
            json.dump(new_params, file, ensure_ascii=False, indent=4)

    def remove_title_parameters(self):
        with open(os.path.join(self.allure_html, "data", "suites.json"), "rb") as file:
            params = json.load(file)

        def remove(node):
            if isinstance(node, dict):
                if "parameters" in node:
                    del node["parameters"]
                for key, value in node.items():
                    remove(value)
            elif isinstance(node, list):
                for item in node:
                    remove(item)
            return node

        new_params = remove(params)
        with open(os.path.join(self.allure_html, "data", "suites.json"), "w", encoding="utf-8") as file:
            json.dump(new_params, file, ensure_ascii=False)

    def save_history_trend(self):
        old_history = os.path.join(self.allure_html, "widgets", "history-trend.json")
        with open(old_history, "rb") as file:
            self.data_json = json.load(file)
        self.max_build = get_max_build_no(self.data_json)
        if self.max_build == 0:
            self.max_build += 1
            self.data_json[-1]["buildOrder"] = self.max_build

    def append_latest_trend(self):
        new_history = os.path.join(self.allure_html, "widgets", "history-trend.json")
        with open(new_history, "rb") as file:
            new_json = json.load(file)
        new_json[0]["buildOrder"] = self.max_build + 1
        self.data_json += new_json
        with open(new_history, "w", encoding="utf-8") as file:
            json.dump(self.data_json, file, ensure_ascii=False, indent=4)

    def open_allure_html(self):
        print()
        subprocess.Popen(f"allure open {self.allure_html}", shell=True)
