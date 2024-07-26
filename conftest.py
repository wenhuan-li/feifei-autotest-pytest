from utils.file_util import get_csv_datas


def pytest_addoption(parser):
    parser.addoption("--csv", action="store", help="Specifies the relative path to the test script file")
    parser.addoption("--scope", action="store", default="smoke,dev,test,stage", help="Specify the scope of use cases to execute")

def pytest_generate_tests(metafunc):
    csv_file = metafunc.config.getoption("csv")
    scope = metafunc.config.getoption("scope").split(",")
    if "case_data" in metafunc.fixturenames:
        cases = get_csv_datas(csv_file, scope)
        ids = [f"Step {case.get('step_id')}: {case.get('step_name')}"
               for case in cases]
        metafunc.parametrize("case_data", cases, ids=ids)
