import pytest


class Hello:

    def __init__(self) -> None:
        pass

    def print_hello(self):
        str = "hello"
        pytest.assume(str == "hello", "hello")
