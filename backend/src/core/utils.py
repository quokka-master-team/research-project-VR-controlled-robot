from datetime import datetime
from importlib import import_module
from typing import Any


def import_from(path: str, name: str) -> Any:
    """
    Import resource from given path with given name
    Args:
        path (str): path to resource module
        name (str): resource name

    Returns:
        resource (Any)
    """

    module = import_module(path)
    return getattr(module, name)


def get_current_time() -> datetime:
    return datetime.utcnow()
