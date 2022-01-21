"""
Test Python script to find a (possibly shortest) path as quickly as possible
from wikipedia page A to B using the wikipedia api
"""
from timeit import default_timer
from wikitas_tools import (
    find_path_wordmatching,
    find_path_wordmatching_parallel,
    find_path_simple,
    find_path_simple_parallel,
    log_path,
)


TEST_SEP = "------------------------------------"

START_PAGE = "amon goth"
END_PAGE = "japan"

# Other examples
# -------------
# START_PAGE = "minami (singer)"
# END_PAGE = "Recall_election"
# END_PAGE = "flyingdog"
# -------------

def test_word_matching_parallel():
    print("With word matching (multi-threaded):")
    print(TEST_SEP)

    try:
        start_1 = default_timer()
        path = find_path_wordmatching_parallel(START_PAGE, END_PAGE)
        end_1 = default_timer()
        dur_1 = end_1 - start_1
        log_path(path)
        print(f"found in {dur_1} s")
    except KeyboardInterrupt:
        end_1 = default_timer()
        print(f"stopped at {end_1 - start_1} s")

    print(TEST_SEP)


def test_word_matching():
    print("With word matching (single thread):")
    print(TEST_SEP)

    try:
        start_1 = default_timer()
        path = find_path_wordmatching(START_PAGE, END_PAGE)
        end_1 = default_timer()
        dur_1 = end_1 - start_1
        log_path(path)
        print(f"found in {dur_1} s")
    except KeyboardInterrupt:
        end_1 = default_timer()
        print(f"stopped at {end_1 - start_1} s")

    print(TEST_SEP)


def test_simple_parallel():
    print("With no matching (multi-threaded)")
    print(TEST_SEP)

    try:
        start_1 = default_timer()
        path = find_path_simple_parallel(START_PAGE, END_PAGE)
        end_1 = default_timer()
        dur_1 = end_1 - start_1
        log_path(path)
        print(f"found in {dur_1} s")
    except KeyboardInterrupt:
        end_1 = default_timer()
        print(f"stopped at {end_1 - start_1} s")

    print(TEST_SEP)


def test_simple():
    print("With no matching (single thread)")
    print(TEST_SEP)

    try:
        start_2 = default_timer()
        path = find_path_simple(START_PAGE, END_PAGE)
        end_2 = default_timer()
        log_path(path)
        print(f"found in {end_2 - start_2} s")
    except KeyboardInterrupt:
        end_2 = default_timer()
        print(f"stopped at {end_2 - start_2} s")

    print(TEST_SEP)


def main():
    test_word_matching_parallel()
    test_simple_parallel()
    test_word_matching()
    test_simple()


if __name__ == "__main__":
    main()
