import os
import re
import shutil
import threading
import time
from utils.allure_util import AllureUtil
from utils.file_util import get_csv_datas

allure_path = None
allure_util = None
report_time = None


def pytest_addoption(parser):
    parser.addoption("--csv", action="store", help="Specifies the relative path to the test script file")
    parser.addoption("--scope", action="store", default="smoke,dev,test,stage",
                     help="Specify the scope of use cases to execute")


# def pytest_configure(config):
#     global allure_path, allure_util
#     file_dir = config.getoption("file_or_dir")
#     report_time = time.strftime("%Y%m%d%H%M")
#     file_name = report_time if not file_dir else re.search(r"([^/\\]+)\.py", file_dir[0]).group(1)
#     allure_path = os.path.join(config.rootdir, "report", file_name)
#     if not os.path.exists(allure_path):
#         os.makedirs(allure_path)
#     else:
#         old_history = os.path.join(allure_path, "html", "widgets", "history-trend.json")
#         if os.path.exists(old_history):
#             allure_util = AllureUtil(config.rootdir, allure_path)
#             allure_util.save_history_trend()
#     if not hasattr(config, "workerinput"):
#         shutil.rmtree(allure_path)
#     worker_id = threading.current_thread().ident
#     worker_dir = os.path.join(allure_path, f"worker_{worker_id}")
#     os.makedirs(worker_dir)
#     config.option.allure_report_dir = worker_dir
#
#
# def pytest_unconfigure(config):
#     global allure_util, allure_path
#     if not hasattr(config, "workerinput"):
#         worker_dirs = [f for f in os.listdir(allure_path) if f.startswith("worker_")]
#         for _dir in worker_dirs:
#             worker_dir = os.path.join(allure_path, _dir)
#             for file in os.listdir(worker_dir):
#                 src = os.path.join(worker_dir, file)
#                 dst = os.path.join(allure_path, file)
#                 shutil.copy(src, dst)
#         for _dir in worker_dirs:
#             shutil.rmtree(os.path.join(allure_path, _dir))
#         title = os.path.basename(allure_path)
#         if allure_util is None:
#             allure_util = AllureUtil(config.rootdir, allure_path)
#         allure_util.add_categories()
#         allure_util.add_environment()
#         allure_util.generate_report()
#         allure_util.remove_title_parameters()
#         allure_util.change_windows_title(title)
#         allure_util.change_summary_title(title)
#         allure_util.append_latest_trend()
#         # allure_comm.open_allure_html()
#

def pytest_configure(config):
    global allure_path, allure_util
    file_dir = config.getoption("file_or_dir")
    report_time = time.strftime("%Y%m%d%H%M")
    file_name = report_time if not file_dir else re.search(r"([^/\\]+)\.py", file_dir[0]).group(1)
    allure_path = os.path.join(config.rootdir, "report", file_name)
    if not os.path.exists(allure_path):
        os.makedirs(allure_path)
    else:
        old_history = os.path.join(allure_path, "html", "widgets", "history-trend.json")
        if os.path.exists(old_history):
            allure_util = AllureUtil(config.rootdir, allure_path)
            allure_util.save_history_trend()
    if not hasattr(config, "workerinput"):
        shutil.rmtree(allure_path)
    worker_id = threading.current_thread().ident
    worker_dir = os.path.join(allure_path, f"worker_{worker_id}")
    os.makedirs(worker_dir)
    config.option.allure_report_dir = worker_dir


def pytest_unconfigure(config):
    global allure_path, allure_util
    if not hasattr(config, "workerinput"):
        worker_dirs = [f for f in os.listdir(allure_path) if f.startswith("worker_")]
        for _dir in worker_dirs:
            worker_dir = os.path.join(allure_path, _dir)
            for file in os.listdir(worker_dir):
                src = os.path.join(worker_dir, file)
                dst = os.path.join(allure_path, file)
                shutil.copy(src, dst)
        for _dir in worker_dirs:
            shutil.rmtree(os.path.join(allure_path, _dir))
        title = os.path.basename(allure_path)
        if allure_util is None:
            allure_util = AllureUtil(config.rootdir, allure_path)
        allure_util.add_categories()
        allure_util.add_environment()
        allure_util.generate_report()
        allure_util.remove_title_parameters()
        allure_util.change_windows_title(title)
        allure_util.change_summary_title(title)
        allure_util.append_latest_trend()
        # allure_comm.open_allure_html()


def pytest_generate_tests(metafunc):
    csv_file = metafunc.config.getoption("csv")
    scope = metafunc.config.getoption("scope").split(",")
    if "case_data" in metafunc.fixturenames:
        cases = get_csv_datas(csv_file, scope)
        ids = [f"Step {case.get('step_id')}: {case.get('step_name')}"
               for case in cases]
        metafunc.parametrize("case_data", cases, ids=ids)
