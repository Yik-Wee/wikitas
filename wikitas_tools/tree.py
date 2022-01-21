"""
Simplified Tree data structure for wiki pathfinding
"""
from typing import Any, Optional, List


class Tree:
    """
    Simplified Tree data structure for wikipedia speedrunning purposes

    Attributes:
    ----------
    `root`: str
        The title of the page link in the case of wikipedia
    `parent`: Tree
        The parent node (Tree)
    `children`: List[Tree]
        The children of Tree
    # `visited`: bool
    #     Whether the node was visited yet (during search)

    Methods:
    -------
    `add_child(child: Tree)`: None
        Adds child to the root of the Tree
    `parents()` : List[str]
        Returns the list of (titles/roots of) parents of the root node (Tree)
        from furthest to closest in depth, not including itself
    """

    def __init__(self, root: Any, parent: Optional['Tree'] = None):
        self.root: Any = root
        self.parent: Tree = parent
        self.children: List[Tree] = []
        # self.visited = False

    def add_child(self, branch: 'Tree') -> None:
        """
        Adds `child` to the root of the Tree
        Returns the child node/branch (Tree)
        """
        branch.parent = self
        self.children.append(branch)

    def parents(self) -> List[str]:
        """
        Returns the list of parents of the root node (Tree)
        from furthest to closest in depth, not including itself
        e.g.
            for Tree A -> B -> C -> self
            Returns [A, B, C]
        """
        path = []
        tree = self

        # Get parents from closest to furthest in depth from self
        while tree.parent is not None:
            path.append(tree.root)
            tree = tree.parent

        path.reverse()  # Convert to furthest to closest (correct order)
        return path

    def __repr__(self):
        return f"Tree({self.root}, {self.parent})"
