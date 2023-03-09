import inspect
import sys
import typing as T

from funcdesc import Description

from .config import CLIConfig, config_to_desc
from .runner import ProcessRunner
from .cmd import Command


def compose_signature(desc: Description) -> inspect.Signature:
    parameters = []
    for arg in desc.inputs:
        param = inspect.Parameter(
            arg.name, inspect.Parameter.POSITIONAL_OR_KEYWORD,
            default=arg.default, annotation=arg)
        parameters.append(param)
    sig = inspect.Signature(parameters)
    return sig


def replace_vals(vals: dict, desc: Description) -> dict:
    vals = vals.copy()
    name_to_arg = {v.name: v for v in desc.inputs}
    for key, val in vals.items():
        arg_obj = name_to_arg[key]
        if (val is True) and ('true_insert' in arg_obj.kwargs):
            vals[key] = arg_obj.kwargs['true_insert']
        if (val is False) and ('false_insert' in arg_obj.kwargs):
            vals[key] = arg_obj.kwargs['false_insert']
    return vals


class cmd2func(object):
    def __init__(
            self, command: str,
            config: T.Optional[CLIConfig] = None,
            print_cmd=True,
            capture_stdout=False,
            capture_stderr=False,
            print_stdout=True,
            print_stderr=True):
        self.command = Command(command)
        if config is None:
            config = self.command.infer_config()
        else:
            config = self.command.complete_config(config)
        self.config = config
        self.desc = config_to_desc(config)
        self.command.check_placeholder([v.name for v in self.desc.inputs])
        self.__signature__ = compose_signature(self.desc)
        self.is_print_cmd = print_cmd
        self.capture_stdout = capture_stdout
        self.capture_stderr = capture_stderr
        self.print_stdout = print_stdout
        self.print_stderr = print_stderr
        self._stdout_content: T.List[str] = []
        self._stderr_content: T.List[str] = []

    @property
    def stdout(self) -> T.Optional[str]:
        if self.capture_stdout:
            return "".join(self._stdout_content)
        else:
            return None

    @property
    def stderr(self) -> T.Optional[str]:
        if self.capture_stderr:
            return "".join(self._stderr_content)
        else:
            return None

    def __call__(self, *args, **kwargs) -> int:
        vals = self.desc.parse_pass_in(args, kwargs)
        vals = replace_vals(vals, self.desc)
        cmd_str = self.command.format(vals)
        if self.is_print_cmd:
            print(f"Run command: {cmd_str}")
        runner = ProcessRunner(cmd_str)
        runner.run()
        g = runner.stream()
        retcode = None
        while True:
            try:
                src, line = next(g)
                if src == 'stdout':
                    if self.print_stdout:
                        print(line.rstrip("\n"))
                    if self.capture_stdout:
                        self._stdout_content.append(line)
                else:
                    if self.print_stderr:
                        print(line.rstrip("\n"), file=sys.stderr)
                    if self.capture_stderr:
                        self._stderr_content.append(line)
            except StopIteration as e:
                retcode = e.value
                break
        return retcode
