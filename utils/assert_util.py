import allure
import pytest


def assert_list(actual_list, expect_list, description=None, message=""):
    for i in range(len(actual_list)):
        actual_dict = actual_list[i]
        expect_dict = expect_list[i]
        assert_dict(actual_dict, expect_dict, description, message)


def assert_dict(actual_dict, expect_dict, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"#### {description}")
    for key, actual in actual_dict.items():
        if key not in expect_dict:
            continue
        expect = expect_dict.get(key)
        if not actual and not expect:
            continue

        _message = f"Test {key}: {actual} | {expect}\t{message}"
        print(_message)
        with allure.step(_message):
            pytest.assume(actual == expect, _message)


def assert_string(actual, expect, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"#### {description}")
    _message = f"Test: {actual} | {expect}\t{message}"
    with allure.step(_message):
        pytest.assume(actual == expect, _message)


def assert_none(expect, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"#### {description}")
    _message = f"Data not found is right\t{message}"
    print(_message)
    with allure.step(_message):
        pytest.assume(expect is None, _message)
