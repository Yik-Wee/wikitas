"""
Functions to interface with the wikipedia api
"""
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import requests
from .tree import Tree

MAX_THREADS = 32

session = requests.Session()
session.mount(
    'https://',
    requests.adapters.HTTPAdapter(pool_maxsize=MAX_THREADS)  # max 8 threads
)
URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "format": "json",
    "prop": "links",
    "pllimit": "max",
}
PARAMS_OPENSEARCH = {
    "action": "opensearch",
    "limit": "max",
    "namespace": "0",
    "format": "json",
}
PARAMS_CATEGORIES = {
    "action": "query",
    "format": "json",
    "prop": "categories",
}


class TitleNotFoundError(Exception):
    def __init__(self, title: str, res: list) -> None:
        super().__init__(f"Title '{title}' is not a valid Wikipedia page.\nWikipedia response: {res}")


def wikititle(title: str) -> str:
    """
    Convert `title` to existing wikipedia title using wikimedia's opensearch
    https://en.wikipedia.org/w/api.php?action=opensearch&search={title}&limit=max&namespace=0&format=json

    e.g. wikititle('among us') -> 'Among_Us'
    
    Raises:
    ------
        `TitleNotFoundError` - if there are no close matches to the invalid wikipedia `title`
    """
    params = {
        **PARAMS_OPENSEARCH,
        "search": title,
    }
    res = session.get(URL, params=params).json()
    # e.g. 'among us' -> [
    #   'Among Us', 'Among Us Hide...', 'They Are Among Us', ...
    # ]
    possible_results = res[1]
    if not possible_results:
        raise TitleNotFoundError(title, res)
    return possible_results[0]  # return the default search


def get_links(title: str) -> List[str]:
    """
    Get all links with namespace=0 from wikipedia page `title` from
    https://en.wikipedia.org/w/api.php?action=query&format=json&titles={title}&prop=links&pllimit=max
    """
    params = {
        **PARAMS,
        "titles": title
    }

    res = session.get(URL, params=params).json()
    page_links = []

    for (_page, contents) in res["query"]["pages"].items():
        links = contents.get("links")
        # Wikipedia page doesn't exist (e.g. Zip_File) -> no links
        if not links:
            continue

        for link in links:
            # Ignore namespaces e.g. "Wikipedia:*", "Help:*", etc.
            if link["ns"] == 0:
                page_links.append(link["title"])

    return page_links


def get_categories(title: str) -> List[str]:
    """
    Gets the categories of the wikipedia page `title` from
    https://en.wikipedia.org/w/api.php?action=query&format=json&titles={title}&prop=categories
    """
    params = {
        **PARAMS_CATEGORIES,
        "titles": title,
    }
    res = session.get(URL, params=params).json()
    page_cats = []

    for (_page, contents) in res["query"]["pages"].items():
        cats = contents.get("categories")
        # Wikipedia page doesn't exist (e.g. Zip_File) -> no links
        if not cats:
            continue

        for cat in cats:
            page_cats.append(cat["title"])

    return page_cats


# ------------------------------------------------------
# Handling of http reqs on multiple threads for speed as
# most of the time 'pathfinding' is spent on http reqs


def _get_links_with_page(page: Tree) -> List[str]:
    """
    Helper for `get_links_parallel`.
    Returns page and links as a tuple:
        (page, links)
    """
    return (page, get_links(page.root))


def get_links_parallel(pages: List[Tree]) -> List[Dict]:
    """
    Get links from `pages` using parallel threads to make http reqs.
    Returns a list in the form of:
        [
            {
                "page": {Tree},
                "links": [...],
            },
            ...
        ]
    """
    # titles_links = defaultdict(list)
    links_pages_list = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for page, links in executor.map(_get_links_with_page, pages):
            # create page-links obj and append to links
            links_pages_list.append({
                "page": page,
                "links": links,
            })

    return links_pages_list
