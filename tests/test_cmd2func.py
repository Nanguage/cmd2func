import pytest
from cmd2func import cmd2func


def test_cmd2func():
    func1 = cmd2func(
        "python -c 'print({a} + {b})'"
    )
    assert func1(1, 2) == 0

    func2 = cmd2func(
        "python -c 'raise IOError(\"test\")'"
    )
    assert func2() > 0

    func3 = cmd2func(
        "python -c 'print({a} + {b})'",
        config={
            "inputs": {
                "a": {
                    "type": "int",
                },
                "b": {
                    "type": "int",
                    "default": 10,
                }
            }
        }
    )
    assert func3(1) == 0
