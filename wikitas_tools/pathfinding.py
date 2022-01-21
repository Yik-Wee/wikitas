"""
Different functions to find (possibly shortest) paths from
wikipedia page A to page B
"""
from typing import List, Optional
from .tree import Tree
from .wikiapi import wikititle, get_links, get_links_parallel
from .word_utils import similarity, get_words, get_words_with_categories
from .wikilog import log_page


def find_path_simple(start: str, dest: str) -> List[str]:
    """
    Finds the shortest path from `start` to `dest` using breadth first seacrh
    Generally faster than `find_path_short` for shorter paths and paths where
    the words in `dest` are not in the wordnet db
    (e.g. Minami (singer) -> Saitama Prefecture || Vietnam War -> Among Us)
    """
    # Convert to valid/existing wikipedia titles
    start_title = wikititle(start)
    dest_title = wikititle(dest)
    if start_title == dest_title:
        return []
    print(f"Finding path from {start_title} to {dest_title}")

    # Initialise queue and tree for BFS
    queue = [Tree(start_title)]
    visited = {start_title}

    # Start BFS
    while queue:  # while queue not empty
        current_page = queue.pop()
        log_page(current_page.root)
        # if current_page.visited:
        #     print("vitied", current_page.root)
        #     continue

        page_links = get_links(current_page.root)
        for link in page_links:
            if link == dest_title:
                return [start_title, *current_page.parents(), dest_title]

            if link not in visited:
                visited.add(link)
                branch = Tree(link)
                current_page.add_child(branch)
                queue.insert(0, branch)

        # current_page.visited = True

    return []


def find_path_wordmatching(start: str, dest: str, top_n: Optional[int] = 7) -> List[str]:
    """
    Finds the (possibly shortest) path from wikipedia page
    `start` to `dest` by comparing the relatedness of words
    in the links to words & categories of `dest`

    Generally takes less time than `find_path_simple` for longer paths and
    paths where words in `dest` are in the wordnet db
    (e.g. Among Us -> Black Hole)
    """
    # Convert to valid/existing wikipedia titles
    start_title = wikititle(start)
    dest_title = wikititle(dest)
    if start_title == dest_title:
        return []

    print(f"Finding path from {start_title} to {dest_title}")

    # dest_words = get_words(dest_title)
    dest_words = get_words_with_categories(dest_title)
    print(f"Matching links against {dest_words}")

    # Initialise queue and tree for BFS
    queue = [Tree(start_title)]
    visited = {start_title}

    # Start BFS
    while queue:  # while queue not empty
        links_by_sim = []
        current_page = queue.pop()
        log_page(current_page.root)
        # if current_page.visited:
        #     print("visited", current_page.root)
        #     continue

        page_links = get_links(current_page.root)
        if not page_links:
            continue

        for link in page_links:
            if link == dest_title:
                return [start_title, *current_page.parents(), dest_title]

            if link not in visited:
                sim = similarity(get_words(link), dest_words)
                visited.add(link)
                links_by_sim.append((link, sim))

        # Filter out the top n (default 7) links by similarity to desitnation word(s)
        links_by_sim.sort(key=lambda x: x[1], reverse=True)
        filtered_links = reversed(links_by_sim[:top_n])  # originally 11

        # Reverse so most recent element in queue (to pop)
        # is highest similarity
        for filtered_link, sim in filtered_links:
            branch = Tree(filtered_link)
            current_page.add_child(branch)
            queue.insert(0, branch)

        # current_page.visited = True

    return []


def find_path_simple_parallel(start: str, dest: str) -> List[str]:
    """
    `find_path_simple()` but http reqs are done in parallel
    """
    start_title = wikititle(start)
    dest_title = wikititle(dest)
    if start_title == dest_title:
        return []
    print(f"Finding path from {start_title} to {dest_title}")

    # Initialise queue and tree for BFS
    queue = [Tree(start_title)]
    visited = {start_title}
    pages_at_once = 32

    # Start BFS
    while queue:  # while queue not empty
        pages: List[str] = []
        for _ in range(pages_at_once):
            if not queue:
                break
            current_page = queue.pop()
            # while current_page.visited:
            #     current_page = queue.pop()
            pages.append(current_page)
            # current_page.visited = True

        parallel_links = get_links_parallel(pages)

        for page_link_obj in parallel_links:
            page = page_link_obj["page"]
            links = page_link_obj["links"]
            log_page(page.root)

            for link in links:
                if link == dest_title:
                    return [start_title, *page.parents(), dest_title]

                if link not in visited:
                    visited.add(link)
                    branch = Tree(link)
                    page.add_child(branch)
                    queue.insert(0, branch)

    return []


def find_path_wordmatching_parallel(start: str, dest: str, top_n: Optional[int] = 7) -> List[str]:
    """
    `find_path_wordmatching()` but http reqs are done in parallel
    """
    # Convert to valid/existing wikipedia titles
    start = wikititle(start)
    dest = wikititle(dest)
    if start == dest:
        return []

    print(f"Finding path from {start} to {dest}")

    # dest_words = get_words(dest_title)
    dest_words = get_words_with_categories(dest)
    print(f"Matching links against {dest_words}")

    # Initialise queue and tree for BFS
    queue = [Tree(start)]
    visited = {start}
    pages_at_once = 32

    # Start BFS
    while queue:  # while queue not empty
        links_by_sim = []
        pages: List[str] = []
        for _ in range(pages_at_once):
            if not queue:
                break
            current_page = queue.pop()
            # while current_page.visited:
            #     current_page = queue.pop()
            pages.append(current_page)
            # current_page.visited = True

        parallel_links = get_links_parallel(pages)

        for page_link_obj in parallel_links:
            page = page_link_obj["page"]
            links = page_link_obj["links"]

            log_page(page.root)

            for link in links:
                if link == dest:
                    return [start, *page.parents(), dest]

                if link not in visited:
                    sim = similarity(get_words(link), dest_words)
                    visited.add(link)
                    links_by_sim.append((link, sim))

            # Filter out the top n (default 7) links by similarity to desitnation word(s)
            links_by_sim.sort(key=lambda x: x[1], reverse=True)
            filtered_links = reversed(links_by_sim[:top_n])  # originally 11

            for filtered_link, sim in filtered_links:
                branch = Tree(filtered_link)
                page.add_child(branch)
                queue.insert(0, branch)

    return []
