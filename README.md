<div align="center">
<h1> cmd2func </h1>

<p> Convert command to callable Python object. </p>

<p>
    <a href="https://github.com/Nanguage/cmd2func/actions/workflows/build_and_test.yml">
        <img src="https://github.com/Nanguage/cmd2func/actions/workflows/build_and_test.yml/badge.svg" alt="Build Status">
    </a>
    <a href="https://app.codecov.io/gh/Nanguage/cmd2func">
        <img src="https://codecov.io/gh/Nanguage/cmd2func/branch/master/graph/badge.svg" alt="codecov">
    </a>
  <a href="https://pypi.org/project/cmd2func/">
    <img src="https://img.shields.io/pypi/v/cmd2func.svg" alt="Install with PyPi" />
  </a>
  <a href="https://github.com/Nanguage/cmd2func/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Nanguage/cmd2func" alt="MIT license" />
  </a>
</p>
</div>

cmd2func is a Python package that allows you to convert command line into Python functions. With cmd2func, you can easily convert common shell commands into Python functions, which can be called in your Python program, making your Python code more flexible and portable.

cmd2func also supports capturing the stdout and stderr of the command line, allowing you to handle command line output easily in Python.


## Features

+ Converts command line into Python functions, making your Python program more flexible and portable.
+ Supports capturing the stdout and stderr of the command line, allowing you to handle command line output easily in Python.
+ Has a simple API, easy to use and integrate into your Python projects.
+ Tested for different operating systems, ensuring that it works well in various environments.

## Installation

```bash
$ pip install cmd2func
```

## Usage examples

### Basic usage

There are three ways to use `cmd2func`:

1. Passing the a command line template string.
2. Use `cmd2func` as a decorator to decorate a function that returns a command line string.
3. Use `cmd2func` as a decorator to decorate a generator function that yield command line strings.

#### Use command line template string

```Python
from cmd2func import cmd2func

myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
)

ret_code = myfunc(1, 2)  # will print '3'
assert ret_code == 0
```

#### Use `cmd2func` as a decorator

`cmd2func` can also be used as a decorator to decorate a function that returns a command line string:

```Python
from cmd2func import cmd2func

@cmd2func
def print_sum(a, b):
    return f"python -c 'print({a} + {b})'"

ret_code = print_sum(1, 2)  # will print '3'
assert ret_code == 0
```

#### Decorate a generator function

`cmd2func` can also be used to decorate a generator function that yield command line strings.
In this way, you can execute multiple commands in a single function call and control the return value of the function:

```Python
from cmd2func import cmd2func

@cmd2func
def print_sum_and_product(a, b):
    ret_code1 = yield f"python -c 'print({a} + {b})'"
    ret_code2 = yield f"python -c 'print({a} * {b})'"
    return ret_code1 + ret_code2

ret_code = print_sum_and_product(2, 3)  # will print '5' and '6'
assert ret_code == 0
```

### Advanced usage

#### Settings for template string

Add default value to argument:

```Python
myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    config={
        'inputs': {
            'b': {
                'type': 'int',
                'default': 10,
            }
        }
    }
)

my_func(1)  # will print '11'
```

Flag argument:

```Python
myfunc = cmd2func(
    "python {verbose} -c 'print({a} + {b})'",
    config={
        'inputs': {
            'verbose': {
                'type': 'bool',
                'true_insert': '-v',
                'false_insert': '',
            }
        },
        'inputs_order': ['a', 'b', 'verbose']
    }
)

myfunc(1, 1, True)  # will print '2' and verbose information
```

#### Settings for print command line

Not print the command:

```Python
myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    print_cmd=False
)

myfunc(1, 2)  # will print '3'
```

#### Capture `stdout` / `stderr`

You can specify a file object to `out_stream` or `err_stream` to capture the `stdout` / `stderr` with cmd2func:

```Python
from io import StringIO

buffer = StringIO()

myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    out_stream=buffer,
)

myfunc(1, 2)
assert buffer.getvalue().strip() == '3'
```

If you want to output to the command line and capture `stdout` / `stderr` at the same time, you can use the `Tee` object provided by cmd2func:

```Python
from io import StringIO
import sys
from cmd2func.utils import Tee

out = StringIO()
t = Tee(sys.stdout, out)
func = cmd2func("python -c 'print({a} + {b})'", out_stream=t)
func(1, 2)  # will print "3"
assert out.getvalue().strip() == "3"
```

#### Steamable command line runner

`cmd2func.runner.ProcessRunner` is a streamable command line runner, which can be used to run command line in a streaming way.

```Python
from cmd2func.runner import ProcessRunner

# run command line and print the output line by line
runner = ProcessRunner("python -c 'print(1 + 2)'")
for (src, line) in runner.steam:
    if src == 'stdout':
        print(line)

# run command line and capture the output and error
from io import StringIO
runner = ProcessRunner("python -c 'print(1 + 2)'")
out, err = StringIO(), StringIO()
runner.write_stream_until_stop(out, err)
print(out.getvalue().strip())  # will print '3'
```
