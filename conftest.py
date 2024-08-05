import os
import re
import shutil
import threading
import time

import allure
import pytest
from playwright.sync_api import sync_playwright
from pywinauto import Application

from utils.allure_util import AllureUtil
from utils.file_util import get_csv_datas


allure_path = None
allure_comm = None


def pytest_addoption(parser):
    parser.addoption("--csv", action="store", help="Specifies the relative path to the test script file")
    parser.addoption("--scope", action="store", default="smoke,dev,test,stage",
                     help="Specify the scope of use cases to execute")
    parser.addoption("--headless", action="store_true",
                     help="Specifies whether to enable headless mode during interface testing")
    parser.addoption("--slowtime", action="store", default=1000,
                     help="Specifies the global delay time for interface testing")


# def pytest_configure(config):
#     global allure_path, allure_comm
#     file_dir = config.getoption("file_or_dir")
#     report_time = time.strftime("%Y%m%d%H%M")
#     file_name = report_time if not file_dir else re.search(r"([^/\\]+)\.py", file_dir[0]).group(1)
#     allure_path = os.path.join(config.rootdir, "target", "report", file_name)
#     if not os.path.exists(allure_path):
#         os.makedirs(allure_path)
#     else:
#         old_history = os.path.join(allure_path, "html", "widgets", "history-trend.json")
#         if os.path.exists(old_history):
#             allure_comm = AllureUtil(config.rootdir, allure_path)
#             allure_comm.save_history_trend()
#     if not hasattr(config, "workerinput"):
#         shutil.rmtree(allure_path)
#     worker_id = threading.current_thread().ident
#     worker_dir = os.path.join(allure_path, f"worker_{worker_id}")
#     os.makedirs(worker_dir)
#     config.option.allure_report_dir = worker_dir
#
#
# def pytest_unconfigure(config):
#     global allure_comm
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
#         if allure_comm is None:
#             allure_comm = AllureUtil(config.rootdir, allure_path)
#         allure_comm.add_categories()
#         allure_comm.add_environment()
#         allure_comm.generate_report()
#         allure_comm.remove_title_parameters()
#         allure_comm.change_windows_title(title)
#         allure_comm.change_summary_title(title)
#         allure_comm.append_latest_trend()
#         # allure_comm.open_allure_html()


def pytest_generate_tests(metafunc):
    csv_file = metafunc.config.getoption("csv")
    scope = metafunc.config.getoption("scope").split(",")
    if "case_data" in metafunc.fixturenames:
        cases = get_csv_datas(csv_file, scope)
        ids = [f"STEP {case.get('step_id')}: {case.get('step_name')}" for case in cases]
        metafunc.parametrize("case_data", cases, ids=ids)


def pytest_collection_modifyitems(session, config, items):
    run_items = []
    for item in items:
        method = item.callspec.params.get("case_data").get("method")
        if item.originalname == method:
            run_items.append(item)
    items[:] = run_items


@pytest.fixture(scope="module")
def playwright_context(request):
    headless = request.config.getoption("--headless")
    slowtime = request.config.getoption("--slowtime")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            slow_mo=float(slowtime)
        )
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


@pytest.fixture(scope="module")
def page(playwright_context):
    page = playwright_context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            case_id = item.callspec.params.get("case_data").get("case_id")
            step_id = item.callspec.params.get("case_data").get("step_id")
            image_name = f"case_{case_id}_step_{step_id}.png"
            screenshot_path = f"../target/screenshot/{image_name}"
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name="screenshot", attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="module")
def app():
    return Application()
