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

Convert command line to a callable object:

```Python
from cmd2func import cmd2func

myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
)

ret_code = myfunc(1, 2)  # will print '3'
print(ret_code)  # will print '0'
```

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

myfunc(1, 1)  # will print '2' and verbose information
```

Not print the command:

```Python
myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    print_cmd=False
)

myfunc(1, 2)  # will print '3'
```

Capture stdout / stderr:

```Python
myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    capture_stdout=True,
)

myfunc(1, 2)  # will print '3'
assert myfunc.stdout.strip() == '3'
```

Not print the stdout / stderr:

```Python
myfunc = cmd2func(
    "python -c 'print({a} + {b})'",
    capture_stdout=True,
    print_stdout=False,
)

myfunc(1, 2)  # will print nothing
assert myfunc.stdout.strip() == '3'
```

## Credits

This package was created with Cookiecutter and the `Nanguage/cookiecutter-pypackage` project template.

+ Cookiecutter: https://github.com/audreyr/cookiecutter
+ `Nanguage/cookiecutter-pypackage`: https://github.com/Nanguage/cookiecutter-pypackage
