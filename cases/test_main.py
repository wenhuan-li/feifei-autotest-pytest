import importlib
import json

import allure
import pytest

mods_path = "mods"


def test_http_api(case_data):
    instance = None
    allure.dynamic.feature("Feature")
    allure.dynamic.suite(f"Case {case_data.get('case_id')}: {case_data.get('case_name')}")
    allure.dynamic.title(f"Step {case_data.get('step_id')}: {case_data.get('step_name')}")
    print(f"\nTest Case => {case_data}")

    route = case_data.get("route")
    if not route:
        raise ValueError(" => Route is missing")

    last_dot_index = route.rfind(".")
    if last_dot_index == -1:
        raise ValueError(" => Route is invalid. Sample: module.class.method")

    module_path = route[:last_dot_index]
    module_name = route[route.rfind(".", 0, last_dot_index) + 1:last_dot_index]
    method_name = route[last_dot_index + 1:]

    # 加载模块
    if importlib.util.find_spec(f"{mods_path}.{module_path}") is None:
        raise ImportError(f" => Module not found: {module_path}")
    module = importlib.import_module(f"{mods_path}.{module_path}")
    print(f" => Load module {module_path} success")

    # 加载主类
    class_name = "".join(word.capitalize() for word in module_name.split("_"))
    if not hasattr(module, class_name):
        raise AttributeError(f" => Class not found: {class_name}")
    cls = getattr(module, class_name)

    # 生成实例
    if not instance or class_name != type(instance).__name__:
        instance = cls()
    print(f" => Load class  {class_name} success")

    # 加载方法或参数
    if not hasattr(instance, method_name):
        raise AttributeError(f" => Method not found: {method_name}")
    method = getattr(instance, method_name)
    parameter = case_data.get("parameter")
    print(f" => Load method {method_name} success")

    # 调用方法执行测试
    if parameter and len(parameter) > 0:
        parameter = json.loads(parameter)
        method(parameter)
    else:
        method()


def test_page_gui(case_data, page):
    instance = None
    allure.dynamic.feature("Feature")
    allure.dynamic.suite(f"Case {case_data.get('case_id')}: {case_data.get('case_name')}")
    allure.dynamic.title(f"Step {case_data.get('step_id')}: {case_data.get('step_name')}")
    print(f"\nTest Case => {case_data}")

    route = case_data.get("route")
    if not route:
        raise ValueError(" => Route is missing")

    last_dot_index = route.rfind(".")
    if last_dot_index == -1:
        raise ValueError(" => Route is invalid. Sample: module.class.method")

    module_path = route[:last_dot_index]
    module_name = route[route.rfind(".", 0, last_dot_index) + 1:last_dot_index]
    method_name = route[last_dot_index + 1:]

    # 加载模块
    if importlib.util.find_spec(f"{mods_path}.{module_path}") is None:
        raise ImportError(f" => Module not found: {module_path}")
    module = importlib.import_module(f"{mods_path}.{module_path}")
    print(f" => Load module {module_path} success")

    # 加载主类
    class_name = "".join(word.capitalize() for word in module_name.split("_"))
    if not hasattr(module, class_name):
        raise AttributeError(f" => Class not found: {class_name}")
    cls = getattr(module, class_name)

    # 生成实例
    if not instance or class_name != type(instance).__name__:
        instance = cls(page)
    print(f" => Load class  {class_name} success")

    # 加载方法或参数
    if not hasattr(instance, method_name):
        raise AttributeError(f" => Method not found: {method_name}")
    method = getattr(instance, method_name)
    parameter = case_data.get("parameter")
    print(f" => Load method {method_name} success")

    # 调用方法执行测试
    if parameter and len(parameter) > 0:
        parameter = json.loads(parameter)
        method(parameter)
    else:
        method()


def test_app_gui(case_data, app):
    instance = None
    allure.dynamic.feature("Feature")
    allure.dynamic.suite(f"Case {case_data.get('case_id')}: {case_data.get('case_name')}")
    allure.dynamic.title(f"Step {case_data.get('step_id')}: {case_data.get('step_name')}")
    print(f"\nTest Case => {case_data}")

    route = case_data.get("route")
    if not route:
        raise ValueError(" => Route is missing")

    last_dot_index = route.rfind(".")
    if last_dot_index == -1:
        raise ValueError(" => Route is invalid. Sample: module.class.method")

    module_path = route[:last_dot_index]
    module_name = route[route.rfind(".", 0, last_dot_index) + 1:last_dot_index]
    method_name = route[last_dot_index + 1:]

    # 加载模块
    if importlib.util.find_spec(f"{mods_path}.{module_path}") is None:
        raise ImportError(f" => Module not found: {module_path}")
    module = importlib.import_module(f"{mods_path}.{module_path}")
    print(f" => Load module {module_path} success")

    # 加载主类
    class_name = "".join(word.capitalize() for word in module_name.split("_"))
    if not hasattr(module, class_name):
        raise AttributeError(f" => Class not found: {class_name}")
    cls = getattr(module, class_name)

    # 生成实例
    if not instance or class_name != type(instance).__name__:
        instance = cls(app)
    print(f" => Load class  {class_name} success")

    # 加载方法或参数
    if not hasattr(instance, method_name):
        raise AttributeError(f" => Method not found: {method_name}")
    method = getattr(instance, method_name)
    parameter = case_data.get("parameter")
    print(f" => Load method {method_name} success")

    # 调用方法执行测试
    if parameter and len(parameter) > 0:
        parameter = json.loads(parameter)
        method(parameter)
    else:
        method()


if __name__ == "__main__":
    pytest.main()
