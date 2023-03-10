import sys
import io

from cmd2func.utils import Tee
from cmd2func import cmd2func


def test_tee():
    out = io.StringIO()
    err = io.StringIO()
    t = Tee(out, err)
    t.write("test")
    assert out.getvalue() == "test"
    assert err.getvalue() == "test"


def test_print_at_same_time():
    out = io.StringIO()
    t = Tee(sys.stdout, out)
    func = cmd2func("python -c 'print({a} + {b})'", out_stream=t)
    func(1, 2)
    assert out.getvalue().strip() == "3"
