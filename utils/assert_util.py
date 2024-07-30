import allure
import pytest

from utils.basic_util import num_to_str, bool_to_str, time_to_str


def assert_list(actual_list, expect_list, description="", message=None):
    for i in range(len(actual_list)):
        actual_dict = actual_list[i]
        expect_dict = expect_list[i]
        assert_dict(actual_dict, expect_dict, description, message)


def assert_dict(actual_dict, expect_dict, description="", message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"#### Description：{description}")
    for key, actual in actual_dict.items():
        if key not in expect_dict:
            continue
        expect = expect_dict.get(key)
        if not actual and not expect:
            continue

        expect = num_to_str(expect)
        expect = bool_to_str(expect)
        expect = time_to_str(expect)
        _message = f"Test {key}: {actual} | {expect}\t{message}"
        print(_message)
        with allure.step(_message):
            pytest.assume(actual == expect, _message)


def assert_none(expect, description="", message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"#### Description：{description}")
    _message = f"Data not found is right\t{message}"
    print(_message)
    with allure.step(_message):
        pytest.assume(expect is None, _message)
