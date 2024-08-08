import allure
import pytest


def assert_list(actual_list, expect_list, description=None, message=""):
    actual_length = len(actual_list)
    expect_length = len(expect_list)
    if actual_length == 0 or expect_length == 0:
        description = (f"Test Skip! One of the two lists is empty => "
                       f"actual_length: {actual_length} | expect_length: {expect_length}")
        allure.dynamic.description(description)
        pytest.skip(description)
    for i in range(len(actual_list)):
        actual_dict = actual_list[i]
        expect_dict = expect_list[i]
        assert_dict(actual_dict, expect_dict, description, message)


def assert_dict(actual_dict, expect_dict, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"{description}")
    for key, actual in actual_dict.items():
        if key not in expect_dict:
            continue
        expect = expect_dict.get(key)
        if not actual and not expect:
            continue

        _message = f"Test {message if message else ""}\t{key}: {actual} | {expect}"
        print(_message)
        with allure.step(_message):
            pytest.assume(actual == expect, _message)


def assert_string(actual, expect, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"{description}")

    _message = f"Test {message if message else ""}\t{actual} | {expect}"
    print(_message)
    with allure.step(_message):
        pytest.assume(actual == expect, _message)


def assert_none(expect, description=None, message=""):
    if description and len(description) > 0:
        allure.dynamic.description(f"{description}")

    _message = f"{message if message else ''} None is right"
    print(_message)
    with allure.step(_message):
        pytest.assume(expect is None, _message)
