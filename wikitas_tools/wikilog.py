"""
Helper to log the current page nicely during the pathfinding
"""
from os import get_terminal_size as _get_terminal_size
from typing import List


_MAGENTA = "\033[35m"
_RESET = "\033[0m"


def log_page(page: str) -> None:
    """
    Log the page in magenta fg colour, formatted by
    [ Current page: {page} ]
    """
    cols, _lines = _get_terminal_size()
    msg = f"[ Current page: {page} ]"
    print(f"\r{_MAGENTA}{msg:<{cols}}{_RESET}", end="")


def log_path(path: List[str]) -> None:
    """
    Log the `path` in magenta fg colour
    """
    path_display = " -> ".join(path)
    print(f"{_MAGENTA}{path_display}{_RESET}")
