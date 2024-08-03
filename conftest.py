import allure
import pytest
from playwright.sync_api import sync_playwright

from utils.file_util import get_csv_datas


def pytest_addoption(parser):
    parser.addoption("--csv", action="store", help="Specifies the relative path to the test script file")
    parser.addoption("--scope", action="store", default="smoke,dev,test,stage",
                     help="Specify the scope of use cases to execute")
    parser.addoption("--headless", action="store_true",
                     help="Specifies whether to enable headless mode during interface testing")
    parser.addoption("--slowtime", action="store", default=1000,
                     help="Specifies the global delay time for interface testing")


def pytest_generate_tests(metafunc):
    csv_file = metafunc.config.getoption("csv")
    scope = metafunc.config.getoption("scope").split(",")
    if "case_data" in metafunc.fixturenames:
        cases = get_csv_datas(csv_file, scope)
        ids = [f"Step {case.get('step_id')}: {case.get('step_name')}" for case in cases]
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
