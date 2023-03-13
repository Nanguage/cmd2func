import inspect
import sys
import typing as T
import functools

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


class CommandFormater(object):
    def __init__(
            self, command: str,
            config: T.Optional[CLIConfig] = None,
            ) -> None:
        self.command = Command(command)
        if config is None:
            config = self.command.infer_config()
        else:
            config = self.command.complete_config(config)
        self.config = config
        self.desc = config_to_desc(config)
        self.command.check_placeholder([v.name for v in self.desc.inputs])
        self.signature = compose_signature(self.desc)

    def get_cmd_str(self, *args, **kwargs) -> str:
        """Get the command string from the arguments."""
        vals = self.desc.parse_pass_in(args, kwargs)
        vals = replace_vals(vals, self.desc)
        cmd_str = self.command.format(vals)
        return cmd_str


StrFunc = T.Callable[..., str]


class Cmd2Func(object):
    def __init__(
            self, cmd_or_func: T.Union[str, StrFunc],
            config: T.Optional[CLIConfig] = None,
            print_cmd=True,
            out_stream=sys.stdout,
            err_stream=sys.stderr,):
        if isinstance(cmd_or_func, str):
            self.formater = CommandFormater(cmd_or_func, config)
            self.get_cmd_str = self.formater.get_cmd_str
            self.__signature__ = self.formater.signature
        else:
            self.get_cmd_str = cmd_or_func
            functools.update_wrapper(self, cmd_or_func)

        self.is_print_cmd = print_cmd
        self.out_stream = out_stream
        self.err_stream = err_stream

    def run_cmd(self, cmd_str: str) -> int:
        """Run the command and return the return code."""
        runner = ProcessRunner(cmd_str)
        runner.run()
        ret_code = runner.write_stream_until_stop(
            self.out_stream, self.err_stream)
        return ret_code

    def __call__(self, *args, **kwargs) -> int:
        cmd_str = self.get_cmd_str(*args, **kwargs)
        if self.is_print_cmd:
            print(f"Run command: {cmd_str}")
        return self.run_cmd(cmd_str)


def cmd2func(
        cmd_or_func: T.Union[str, StrFunc, None] = None,
        config: T.Optional[CLIConfig] = None,
        print_cmd=True,
        out_stream=sys.stdout,
        err_stream=sys.stderr,
        ) -> Cmd2Func:
    """Convert a command string to a function."""
    if cmd_or_func is None:
        return functools.partial(  # type: ignore
            cmd2func, config=config, print_cmd=print_cmd,
            out_stream=out_stream, err_stream=err_stream)
    else:
        return Cmd2Func(
            cmd_or_func, config, print_cmd, out_stream, err_stream
        )
