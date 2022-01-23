"""
Helper to log the current page nicely during the pathfinding
"""
from typing import Iterable


_MAGENTA_FG = "\033[35m"
_GREEN_FG = "\033[32m"
_RESET = "\033[0m"


def log_page(page: str) -> None:
    """
    Log the page in magenta fg colour, formatted by
    [ Current page: {page} ]
    Overwrites the previous output of log_page()
    """
    print(f"\033[1K\r{_MAGENTA_FG}[ Current page: {page} ]{_RESET}", end="")


def log_path(path: Iterable[str]) -> None:
    """
    Log the `path` in green fg colour, formatted by
    path[0] -> path[1] -> ... -> path[n]
    """
    path_display = " -> ".join(path)
    print(f"{_GREEN_FG}{path_display}{_RESET}")
