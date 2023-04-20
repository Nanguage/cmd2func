import io
import os

import pytest
from cmd2func import cmd2func
from cmd2func.cmd import Command


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
        "python -c 'print({a} + {b} + {c})'",
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
    assert func3(1, c=10) == 0
    with pytest.raises(TypeError):
        func3(1)

    func4 = cmd2func(
        "python {verbose} -c 'print({a} + {b})'",
        config={
            "inputs": {
                "verbose": {
                    "type": "bool",
                    "true_insert": "-v",
                    "false_insert": "",
                }
            },
            "inputs_order": ["a", "b", "verbose"]
        }
    )
    assert func4(1, 2, verbose=True) == 0
    assert func4(1, 2, verbose=False) == 0


def test_cmd2func_2():
    func5 = cmd2func(
        "python -c 'print({a} + {b})'",
        config={
            "inputs": {
                "c": {
                    "type": "int",
                }
            }
        }
    )
    assert func5(1, 2) == 0


def test_type():
    func = cmd2func(
        "python -c 'print({a} + {b})'",
        config={
            "inputs": {
                "a": {
                    "type": "int",
                },
            }
        }
    )
    assert func.formater.desc.inputs[0].type is int


def test_command():
    cmd = Command("python -c 'print({a} + {b})'")
    with pytest.raises(ValueError):
        cmd.format({"a": 1})
    with pytest.raises(ValueError):
        cmd.check_placeholder(["a", "b", "c"])


def test_capture_stdout():
    out = io.StringIO()
    func = cmd2func(
        "python -c 'print({a} + {b})'",
        out_stream=out,
    )
    assert func(1, 2) == 0
    out.seek(0)
    assert out.read().strip() == "3"


def test_capture_stderr():
    err = io.StringIO()
    func = cmd2func(
        "python -c 'raise IOError(\"test\")'",
        err_stream=err,
    )
    assert func(1, 2) > 0
    err.seek(0)
    assert len(err.read().strip()) > 0


def test_as_decorator():
    @cmd2func
    def sum_command(a, b):
        return f'python -c "print({a} + {b})"'

    assert sum_command(1, 2) == 0

    out = io.StringIO()

    @cmd2func(out_stream=out)
    def sum_command(a, b):
        return f'python -c "print({a} + {b})"'

    assert sum_command(1, 2) == 0
    assert out.getvalue().strip() == "3"


def test_decorate_genfunc():
    out = io.StringIO()

    @cmd2func(out_stream=out)
    def sum_and_product(a, b):
        r1 = yield f'python -c "print({a} + {b})"'
        r2 = yield f'python -c "print({a} * {b})"'
        return r1 + r2

    assert sum_and_product(1, 2) == 0
    assert out.getvalue().strip().split() == ["3", "2"]


def test_popen_kwargs():
    out = io.StringIO()
    env = os.environ.copy()
    env.update({'a': 'b'})

    @cmd2func(
        out_stream=out,
        popen_kwargs={'env': env},
    )
    def print_env():
        return 'python -c "import os; print(os.environ[\'a\'])"'

    assert print_env() == 0
    assert out.getvalue().strip() == "b"


def test_conda_env():
    cmd = "python -c 'print(1)'"

    @cmd2func(conda_env="test")
    def test1():
        return cmd

    new_cmd = test1.process_cmd_str(cmd)
    assert new_cmd.startswith(
        "conda run --no-capture-output -n test")
