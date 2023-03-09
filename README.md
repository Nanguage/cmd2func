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

**Work In Progress**


## Features

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

## Credits

This package was created with Cookiecutter and the `Nanguage/cookiecutter-pypackage` project template.

+ Cookiecutter: https://github.com/audreyr/cookiecutter
+ `Nanguage/cookiecutter-pypackage`: https://github.com/Nanguage/cookiecutter-pypackage
