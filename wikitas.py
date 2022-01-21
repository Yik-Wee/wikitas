"""
The main code for the wikitas, passing START_PAGE, END_PAGE and [...OPTIONS] as args
"""
import sys
import timeit
from typing import Callable, Optional
from wikitas_tools import (
    find_path_simple,
    find_path_simple_parallel,
    find_path_wordmatching,
    find_path_wordmatching_parallel,
    log_path,
)


def print_help():
    print("""
DESCRIPTION:
    Find the path from wikipedia page START_PAGE to END_PAGE using different methods.
    All methods use the Breadth-First Search algorithm on the Tree of wikipedia page links

USAGE:
    python3 wikitas.py [START_PAGE] [END_PAGE] [...OPTIONS]

OPTIONS:
    -h | --help             Display this help page
    -w | --matchwords       Find path from START_PAGE to END_PAGE by matching the relatedness of words
    -s | --simple           Find path from START_PAGE to END_PAGE using without matching words
    -Pw | --Pmatchwords     Same as --matchwords but using multi-threaded http requests to the wikipedia api
    -Ps | --Psimple         (Default) Same as --simple but using multi-threaded http requests to the wikipedia api
""")


def run_wikitas(start: str, end: str, callback: Optional[Callable[str, str]] = find_path_simple_parallel) -> None:
    start_time = timeit.default_timer()
    path = callback(start, end)
    end_time = timeit.default_timer()

    log_path(path)
    print(f"Found in {end_time - start_time} s")


def main() -> None:
    args = sys.argv
    args.pop(0)  # Get args from user
    print(args)
    callback_options = set()
    start_end = []

    # Arg parsing
    for arg in args:
        # Match arg against valid options
        if arg in ("-w", "--matchwords"):
            callback_options.add(find_path_wordmatching)
        elif arg in ("-s", "--simple"):
            callback_options.add(find_path_simple)
        elif arg in ("-Pw", "-Pmatchwords"):
            callback_options.add(find_path_wordmatching_parallel)
        elif arg in ("-Ps", "--Psimple"):
            callback_options.add(find_path_simple_parallel)
        elif arg.startswith("-"):  # Invalid option - abort
            print(f"Invalid option: '{arg}'")
            print_help()
            return
        else:  # Arg is start or end page title
            start_end.append(arg)

    if len(start_end) != 2:  # End missing or too many pages passed as args
        print_help()
        return

    start, end = start_end
    if not callback_options:  # No callback option specified - default --Psimple
        run_wikitas(start, end)
        return

    for callback in callback_options:  # Run the wikitas for each callback specified
        run_wikitas(start, end, callback)


if __name__ == "__main__":
    main()
