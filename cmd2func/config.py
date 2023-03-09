import typing as T
import sys
if sys.version_info < (3, 11):
    from typing_extensions import TypedDict, Required, NotRequired
else:
    from typing import TypedDict, Required, NotRequired


from funcdesc.desc import Description, Value, NotDef


class ArgDef(TypedDict):
    type: str
    default: T.Any


class CLIConfig(TypedDict):
    name: NotRequired[str]
    inputs: T.Dict[str, ArgDef]


def extrace_key(d: dict, key, default) -> T.Any:
    if key in d:
        return d.pop(key)
    else:
        return default


def config_to_desc(config: CLIConfig) -> Description:
    """Convert a config to a funcdesc's Description object."""
    args_conf = config['inputs']
    inputs = []
    for n, p_conf in args_conf.items():
        pc: dict = {**p_conf}
        _tp = extrace_key(pc, 'type', None)
        _default = extrace_key(pc, 'default', NotDef)
        val = Value(
            type=eval(_tp),
            range=None,
            default=_default,
            name=n,
            **pc
        )
        inputs.append(val)
    desc = Description(inputs)
    return desc