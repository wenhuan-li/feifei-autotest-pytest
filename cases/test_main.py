import importlib
import json

import allure
import pytest


mods_path = "mods"


def test_main_case(case_data):
    instance = None
    allure.dynamic.suite(f"Case {case_data.get('case_id')}: {case_data.get('case_name')}")
    allure.dynamic.title(f"Step {case_data.get('step_id')}: {case_data.get('step_name')}")
    print(case_data)

    route = case_data.get("route")
    if not route:
        raise ValueError("Route is required")

    last_dot_index = route.rfind(".")
    if last_dot_index == -1:
        raise ValueError("Route format is invalid. Expected format: module.class.method")

    module_path = route[:last_dot_index]
    module_name = route[route.rfind(".", 0, last_dot_index) + 1:last_dot_index]
    method_name = route[last_dot_index + 1:]

    try:
        module = importlib.import_module(f"{mods_path}.{module_path}")
        print(f"Import module: {mods_path}.{module_path} success")

        class_name = "".join(word.capitalize() for word in module_name.split("_"))
        if not hasattr(module, class_name):
            raise AttributeError(f"Class {class_name} not found in module {module_path}")

        cls = getattr(module, class_name)

        if not instance or class_name != type(instance).__name__:
            instance = cls()

        if not hasattr(instance, method_name):
            raise AttributeError(f"Method {method_name} not found in class {class_name}")

        method = getattr(instance, method_name)
        parameter = case_data.get("parameter")

        if parameter and len(parameter) > 0:
            parameter = json.loads(parameter)
            method(parameter)
        else:
            method()

    except ModuleNotFoundError:
        print(f"Module {module_name} not found.")
    except ImportError as e:
        print(f"An error occurred while importing {module_name}: {e}")
    except json.JSONDecodeError as e:
        print(f"Decoding JSON Error: {e}")
    except ValueError as e:
        print(f"ValueError: {e}")
    except AttributeError as e:
        print(f"AttributeError: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    pytest.main()